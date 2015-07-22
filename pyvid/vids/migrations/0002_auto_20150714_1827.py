# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vids.models


class Migration(migrations.Migration):

    dependencies = [
        ('vids', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-pubdate']},
        ),
        migrations.RenameField(
            model_name='video',
            old_name='file',
            new_name='original_video',
        ),
        migrations.AddField(
            model_name='video',
            name='converted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='mp4_720',
            field=models.FileField(null=True, upload_to=vids.models.get_upload_file_name, blank=True),
            preserve_default=True,
        ),
    ]
