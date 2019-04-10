from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Invoice, InvoicePayment
import stripe
import decimal


@user_passes_test(lambda u: u.is_superuser)
def send_invoice(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.prefetch_related('items', 'payments'),
        pk=pk)

    if request.method == 'POST':
        sender = request.POST['sender']
        recipients = [r.strip() for r in request.POST['recipients'].split(',')]
        subject = request.POST['subject']
        html = request.POST['html_body']
        text = request.POST['text_body']

        send_mail(
            subject,
            text,
            sender,
            recipients,
            html_message=html,
            fail_silently=False,
        )

        invoice.has_been_sent = True
        invoice.save()

        messages.success(request, 'Successfully sent invoice!')
        return redirect('admin:payable_invoice_change', pk)

    else:
        invoice_path = reverse('view-invoice', args=[invoice.pk])
        invoice_context = {
            'invoice': invoice,
            'invoice_url': request.build_absolute_uri(invoice_path) + '?key=' + invoice.access_code
        }
        invoice_subject = render_to_string('invoice-subject.txt', invoice_context)
        invoice_html = render_to_string('invoice-email.html', invoice_context)
        invoice_text = render_to_string('invoice-email.txt', invoice_context)

        context = {
            'invoice': invoice,
            'invoice_subject': invoice_subject,
            'invoice_text': invoice_text,
            'invoice_html': invoice_html,

            'opts': Invoice._meta,
            'has_change_permission': True,
            'original': invoice,
        }
        return render(request, 'send-invoice-form.html', context)

def view_invoice(request, pk):
    try:
        access_code = request.GET['key']
    except KeyError:
        raise Http404

    invoice = get_object_or_404(
        Invoice.objects.prefetch_related('items', 'payments'),
        pk=pk, access_code=access_code)

    if 'peek' not in request.GET:
        invoice.has_been_seen = True
        invoice.save()

    context = {'object': invoice, 'invoice': invoice, 'stripe_price': invoice.amount_due() * 100 }
    return render(request, 'invoice.html', context)

def charge_card(request):
    invoice_pk = request.POST['invoice_id']
    access_code = request.POST['access_code']
    stripe_token = request.POST['stripeToken']
    stripe_email = request.POST['stripeEmail']
    stripe.api_key = settings.STRIPE_SECRET_KEY

    invoice = get_object_or_404(
        Invoice.objects.prefetch_related('items', 'payments'),
        pk=invoice_pk, access_code=access_code)

    try:
        charge = stripe.Charge.create(
            amount=int(invoice.amount_due() * 100),
            currency='usd',
            card=stripe_token,
            description=str(invoice),
            metadata={
                'name': invoice.recipient.name,
                'organization': invoice.recipient.organization,
                'email': invoice.recipient.email,
                'phone': invoice.recipient.phone,
                'receipt_email': stripe_email,
                'statement_descriptor': request.POST.get('statement_descriptor', None)
            }
        )
        messages.success(request, 'Thank you for your payment on <i>{}</i>!'.format(invoice))

    except stripe.error.StripeError as e:
        messages.error(request, ('There was an error processing your payment: {}. '
            'Please try again, or contact us if you\'re having trouble.').format(e))

    else:
        invoice.payments.add(InvoicePayment(
            amount=charge.amount / 100,
            paid_at=now(),
            stripe_charge_id=charge.id
        ))

    return HttpResponseRedirect(reverse('view-invoice', kwargs={'pk': '{:0>5}'.format(invoice_pk)}) + '?key=' + access_code)
