# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payable', '0003_add_notes_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoicePayment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('paid_at', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('stripe_charge_id', models.TextField(blank=True)),
                ('invoice', models.ForeignKey(related_name='payments', to='payable.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='amount_paid',
        ),
    ]
