# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payable', '0004_create_model_InvoicePayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='has_been_seen',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
