# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vids', '0002_auto_20150714_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='mp4_720',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
