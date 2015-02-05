# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from .models import Client, Invoice, InvoiceItem


class InvoiceItemInline (admin.TabularInline):
    model = InvoiceItem
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    readonly_fields = ['amount']
    extra = 1

class InvoiceAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    inlines = [InvoiceItemInline]
    raw_id_fields = ['recipient']
    readonly_fields = ['total_amount', 'amount_due', 'access_code', '_preview']

    def _preview(self, obj):
        if not obj.id:
            return '(save to preview)'

        return format_html(
            '''<a href="{}?key={}" target="_blank">Open in new window &#8663</a>''',  # 8663 is the ⇗ character
            reverse('view-invoice', kwargs={'pk': obj.pk}),
            obj.access_code
        )
    _preview.allow_tags = True
    _preview.short_description = _('Preview')


admin.site.register(Client)
admin.site.register(Invoice, InvoiceAdmin)