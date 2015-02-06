# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_abbreviations(apps, schema_editor):
    Client = apps.get_model('payable', 'Client')
    for client in Client.objects.all():
        try:
            invoice = client.invoice_set.all().order_by('-id')[0]
        except IndexError:
            client.abbreviation = client.organization[:3].lower()
        else:
            upper_abbrev, _ = invoice.number.split('-')
            client.abbreviation = upper_abbrev.lower()
        client.save()

def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('payable', '0005_invoice_has_been_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='abbreviation',
            field=models.CharField(default='', max_length=5, help_text='The abbreviation is used in invoice numbers.'),
            preserve_default=False,
        ),
        migrations.RunPython(
            add_abbreviations,
            noop
        )
    ]
