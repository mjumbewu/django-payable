from copy import copy
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
import uuid


class ClonableMixin:
    def copy_relations_to(self, clone, commit=True):
        assert clone.pk is not None, 'You must save the clone before copying related objects.'
        pass

    def copy(self, commit=True, **overrides):
        clone = copy(self)
        clone.pk = None

        for attr, value in overrides.items():
            setattr(clone, attr, value)

        if commit:
            clone.save()
            self.copy_relations_to(clone)

        return clone


class Invoicer (models.Model):
    name = models.TextField()
    address = models.TextField(help_text='At least the address.')
    phone = models.TextField(default='', blank=True)
    email = models.EmailField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return "{}\n{}".format(self.name, self.address)

    def save(self, *args, **kwargs):
        other_defaults = Invoicer.objects.filter(is_default=True).exclude(pk=self.pk)

        if self.is_default:
            # There should be no more than one default
            if other_defaults.exists():
                other_defaults.update(is_default=False)
        else:
            # There should be at least one default
            if not other_defaults.exists():
                self.is_default = True

        return super(Invoicer, self).save(*args, **kwargs)



class Client (models.Model):
    name = models.TextField()
    organization = models.TextField()
    abbreviation = models.CharField(max_length=5, help_text='The abbreviation is used in invoice numbers.')
    address = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    email = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.organization, self.name)


class InvoiceItem (ClonableMixin, models.Model):
    invoice = models.ForeignKey('Invoice', related_name='items', on_delete=models.CASCADE)

    description = models.TextField()
    quantity = models.DecimalField(decimal_places=2, max_digits=12)
    units = models.TextField(blank=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=12)
    notes = models.TextField(blank=True)

    def amount(self):
        return (self.quantity or 0) * (self.unit_price or 0)

    def __str__(self):
        return self.description


class InvoicePayment (models.Model):
    invoice = models.ForeignKey('Invoice', related_name='payments', on_delete=models.CASCADE)
    paid_at = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    stripe_charge_id = models.TextField(blank=True)

    def __str__(self):
        return 'Paid ${} {}'.format(self.amount, naturaltime(self.paid_at))


class Invoice (ClonableMixin, models.Model):
    project = models.TextField(blank=True)
    number = models.TextField(blank=True)
    sent_date = models.DateField()
    due_date = models.DateField()

    sender = models.ForeignKey('Invoicer', related_name='invoices', on_delete=models.CASCADE)
    recipient = models.ForeignKey('Client', related_name='invoices', on_delete=models.CASCADE)
    has_been_sent = models.BooleanField(blank=True, default=False)
    has_been_seen = models.BooleanField(blank=True, default=False)

    # Reverse relation to invoice items
    # Reverse relation to invoice payments

    discount = models.DecimalField(decimal_places=2, max_digits=12, blank=True, default=0)
    additional_notes = models.TextField(blank=True)

    access_code = models.TextField(blank=True)

    def total_amount(self):
        return sum((item.amount() or 0) for item in self.items.all())

    def amount_paid(self):
        return sum((payment.amount or 0) for payment in self.payments.all())

    def amount_due(self):
        return self.total_amount() - (self.discount or 0) - self.amount_paid()

    def is_paid(self):
        return self.amount_due() == 0
    is_paid.boolean = True

    def __str__(self):
        return "Invoice for {} to {} on {} (${:,.2f})".format(self.project or '(unknown project)', self.recipient.organization, self.sent_date, self.total_amount())

    def copy_relations_to(self, clone, commit=True):
        # Only copy the items, not the payments.
        for item in self.items.all():
            item.copy(commit, invoice=clone)

    def copy(self, commit=True, **overrides):
        clone = super().copy(commit=commit, number='', access_code='')
        return clone

    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = uuid.uuid4()

        super().save(*args, **kwargs)

        if not self.number:
            # We use the id to determine the invoice number, so it has to come
            # after the save.
            self.number = '{}-{:0>5}'.format(self.recipient.abbreviation.upper(), self.id)
            self.save()
