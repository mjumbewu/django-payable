from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
import uuid


class Client (models.Model):
    name = models.TextField()
    organization = models.TextField()
    address = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    email = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.organization, self.name)


class InvoiceItem (models.Model):
    invoice = models.ForeignKey('Invoice', related_name='items')

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
    invoice = models.ForeignKey('Invoice', related_name='payments')
    paid_at = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    stripe_charge_id = models.TextField(blank=True)

    def __str__(self):
        return 'Paid ${} {}'.format(self.amount, naturaltime(self.paid_at))


class Invoice (models.Model):
    number = models.TextField(blank=True)
    sent_date = models.DateField()
    due_date = models.DateField()

    recipient = models.ForeignKey('Client')
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
        return "Invoice for {} on {} (${:,.2f})".format(self.recipient.organization, self.sent_date, self.total_amount())

    def save(self):
        super().save()

        dirty = False
        if not self.number:
            self.number = '{}-{:0>5}'.format(self.recipient.organization[:3], self.id)
            dirty = True

        if not self.access_code:
            self.access_code = uuid.uuid4()
            dirty = True

        if dirty:
            self.save()
