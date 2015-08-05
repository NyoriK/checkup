# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vids.models


class Migration(migrations.Migration):

    dependencies = [
        ('vids', '0003_auto_20150715_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='mp4_720',
            field=models.FileField(null=True, upload_to=vids.models.get_upload_file_name, blank=True),
        ),
    ]
