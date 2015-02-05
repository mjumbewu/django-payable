# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='access_code',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
