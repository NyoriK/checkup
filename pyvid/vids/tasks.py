import logging
logger = logging.getLogger(__name__)

import subprocess
from pyvid.celery import app

from time import time
import ntpath

from models import Video

# def get_upload_file_name(video):
#     original_name = str(video.original_video)
#     original_name = ntpath.basename(original_name)
#     return "%s_%s" % (str(time()).replace('.', '_'), original_name)

def get_upload_file_name(video):
    name = video.title
    name = name+'.mp4'
    return name

from pyvid.settings import MEDIA_ROOT

from django.core.files import File

import os


@app.task
def convert_video(video_id):
    video = Video.objects.get(id=video_id)
    video_path = str(MEDIA_ROOT)+'/'+str(video.original_video)
    convert_video_name = get_upload_file_name(video)
    cmd = 'ffmpeg -i %s -codec:v libx264 -profile:v baseline -preset slow -b:v 250k -maxrate 250k -bufsize 500k -vf scale=-1:360 -threads 0 -codec:a libfdk_aac -movflags +faststart %s' % (video_path, convert_video_name)
    subprocess.call(
        cmd,
        shell=True
    )

    fp = open(convert_video_name)
    myfile = File(fp)
    video.mp4_720.save(name=convert_video_name, content=myfile)
    video.converted = True
    video.save()
    os.remove(convert_video_name)