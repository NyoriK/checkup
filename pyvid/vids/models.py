from django.db import models
from django.utils import timezone

from time import time


def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)


class Video(models.Model):
    title = models.CharField(max_length=75)
    pubdate = models.DateTimeField(default=timezone.now)
    original_video = models.FileField(upload_to=get_upload_file_name)
    mp4_720 = models.TextField(blank=True, null=True)
    converted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pubdate']

    def __unicode__(self):
        return ("%s - %s") % (self.pk, self.title)