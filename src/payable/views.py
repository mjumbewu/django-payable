from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Invoice

def view_invoice(request, pk):
    try:
        access_code = request.GET['key']
    except KeyError:
        raise Http404

    invoice = get_object_or_404(Invoice, pk=pk, access_code=access_code)
    context = {'object': invoice, 'invoice': invoice}
    return render(request, 'invoice.html', context)