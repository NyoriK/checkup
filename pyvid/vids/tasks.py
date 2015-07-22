import logging
logger = logging.getLogger(__name__)

import subprocess
from pyvid.celery import app

from time import time
import ntpath

from models import Video

def get_upload_file_name(video):
    original_name = str(video.original_video)
    original_name = ntpath.basename(original_name)
    return "%s_%s" % (str(time()).replace('.', '_'), original_name)


@app.task
def convert_video(video_id):
    video = Video.objects.get(video_id)
    convert_video_name = get_upload_file_name(video)
    # subprocess.call(
    #     'ffmpeg -i %s %s' % (
    #         'http://localhost:8000/media/'+str(video.original_video), convert_video_name ))

    subprocess.call(
        'ffmpeg -analyzeduration 2147483647 -probesize 2147483647 -i %s -pix_fmt yuv420p -vf scale=-2:720 %s' % ('http://localhost:8000/media/'+str(video.original_video), convert_video_name )
    )

    video.mp4_720 = convert_video_name
    video.converted = True
    video.save()