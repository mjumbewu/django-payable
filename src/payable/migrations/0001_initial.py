# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.TextField()),
                ('organization', models.TextField()),
                ('address', models.TextField(blank=True)),
                ('phone', models.TextField(blank=True)),
                ('email', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('number', models.TextField(blank=True)),
                ('sent_date', models.DateField()),
                ('due_date', models.DateField()),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, default=0)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=12, default=0)),
                ('recipient', models.ForeignKey(to='payable.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', models.TextField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('units', models.TextField(blank=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('invoice', models.ForeignKey(related_name='items', to='payable.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
