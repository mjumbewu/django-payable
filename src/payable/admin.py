# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from .models import Client, Invoice, InvoiceItem, InvoicePayment


class ClientAdmin (admin.ModelAdmin):
    prepopulated_fields = {'abbreviation': ('organization',)}


class InvoiceItemInline (admin.TabularInline):
    model = InvoiceItem
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    readonly_fields = ['amount']
    extra = 1


class InvoicePaymentInline (admin.TabularInline):
    model = InvoicePayment
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    exclude = ['stripe_charge_id']
    readonly_fields = ['_stripe_charge']
    extra = 0

    def _stripe_charge(self, obj):
        if not obj.stripe_charge_id:
            return 'paid by check'

        return format_html(
            '''<a href="https://dashboard.stripe.com/test/payments/{0}" target="_blank">{0} &#8663</a>''',  # 8663 is the ⇗ character
            obj.stripe_charge_id
        )
    _stripe_charge.allow_tags = True
    _stripe_charge.short_description = _('Stripe Charge')


class InvoiceAdmin (admin.ModelAdmin):
    list_display = ['__str__', 'has_been_seen', 'is_paid']

    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    inlines = [InvoiceItemInline, InvoicePaymentInline]
    raw_id_fields = ['recipient']
    readonly_fields = ['total_amount', 'amount_paid', 'amount_due', 'access_code', '_preview']

    def _preview(self, obj):
        if not obj.id:
            return '(save to preview)'

        return format_html(
            '''<a href="{}?key={}&peek" target="_blank">Open in new window &#8663</a>''',  # 8663 is the ⇗ character
            reverse('view-invoice', kwargs={'pk': '{:0>5}'.format(obj.pk)}),
            obj.access_code
        )
    _preview.allow_tags = True
    _preview.short_description = _('Preview')


admin.site.register(Client, ClientAdmin)
admin.site.register(Invoice, InvoiceAdmin)