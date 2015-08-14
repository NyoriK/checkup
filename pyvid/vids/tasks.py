import logging
logger = logging.getLogger(__name__)

from pyvid.celery import app

from time import time
# import ntpath

from models import Video

import re

def get_upload_file_name(video):
    original_name = video.title
    # original_name = ntpath.basename(original_name)
    return "%s_%s" % (str(time()).replace('.', '_'), re.sub(r'[^a-zA-Z0-9_-]', '',original_name))

# def get_upload_file_name(video):
#     name = video.title
#     return name

def timer(start_time,end_time):
    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return ("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))    

from pyvid.settings import MEDIA_ROOT, MEDIA_URL

from django.core.files import File

import os

from subprocess import Popen


@app.task
def convert_video(video_id):
    video = Video.objects.get(id=video_id)

    # If on same machine
    video_path = str(MEDIA_ROOT)+'/'+str(video.original_video)

    # # For s3
    # # video_path = video.original_video.url
    # # or
    # video_path = str(MEDIA_URL) + str (video.original_video)

    convert_video_name_720 = '720-'+str(get_upload_file_name(video))+'.mp4'
    convert_video_name_480 = '480-'+str(get_upload_file_name(video))+'.mp4'

    # 720 scale
    # cmd = 'ffmpeg -i %s -codec:v libx264 -profile:v baseline -preset slow -b:v 250k -maxrate 250k -bufsize 500k -vf scale="trunc(oh*a/2)*2:720" -threads 0 -codec:a libfdk_aac -movflags +faststart %s' % (video_path, convert_video_name)
    # with -s hd720 flag
    # cmd = 'ffmpeg -i %s -codec:v libx264 -tune zerolatency -profile:v baseline -level 3.0 -preset medium -crf 23 -maxrate 400k -bufsize 1835k -s hd720 format=yuv420p -threads 0 -codec:a libfdk_aac -movflags +faststart %s' % (video_path, convert_video_name)
    cmd = """
        ffmpeg -i %s \
            -codec:v libx264 -tune zerolatency -profile:v main -preset medium -crf 23 -maxrate 1000k -bufsize 10000k -s hd720 -codec:a libfdk_aac -pix_fmt yuv420p -movflags +faststart -threads 0 %s \
            -codec:v libx264 -tune zerolatency -profile:v main -preset medium -crf 23 -maxrate 500k -bufsize 5000k -s hd480 -codec:a libfdk_aac -pix_fmt yuv420p -movflags +faststart -threads 0 %s
        """ % (video_path, convert_video_name_720, convert_video_name_480)
    start_time = time()
    proc = Popen(
        cmd,
        shell=True
    )
    proc.wait()

    if proc.returncode == 0:
        end_time = time()
        time_taken = timer(start_time, end_time)
        fp_720 = open(convert_video_name_720)
        fp_480 = open(convert_video_name_480)
        myfile_720 = File(fp_720)
        myfile_480 = File(fp_480)
        video.mp4_720.save(name=convert_video_name_720, content=myfile_720)
        video.mp4_480.save(name=convert_video_name_480, content=myfile_480)
        video.time_taken = time_taken
        video.converted = True
        video.save()
        os.remove(convert_video_name_720)
        os.remove(convert_video_name_480)
    else:
        # Do something / Inform user in notification
        pass







# @app.task
# def convert_video(video_id):
#     video = Video.objects.get(id=video_id)

#     # If on same machine
#     # video_path = str(MEDIA_ROOT)+'/'+str(video.original_video)

#     # For s3
#     # video_path = video.original_video.url
#     # or
#     video_path = str(MEDIA_URL) + str (video.original_video)

#     convert_video_name = str(get_upload_file_name(video))+'.mp4'

#     # 720 scale
#     # cmd = 'ffmpeg -i %s -codec:v libx264 -profile:v baseline -preset slow -b:v 250k -maxrate 250k -bufsize 500k -vf scale="trunc(oh*a/2)*2:720" -threads 0 -codec:a libfdk_aac -movflags +faststart %s' % (video_path, convert_video_name)
#     # with -s hd720 flag
#     cmd = 'ffmpeg -i %s -codec:v libx264 -tune zerolatency -profile:v baseline -level 3.0 -preset medium -crf 23 -maxrate 400k -bufsize 1835k -s hd720 format=yuv420p -threads 0 -codec:a libfdk_aac -movflags +faststart %s' % (video_path, convert_video_name)
#     subprocess.Popen(
#         cmd,
#         shell=True
#     )

#     fp = open(convert_video_name)
#     myfile = File(fp)
#     video.mp4_720.save(name=convert_video_name, content=myfile)
#     video.converted = video.converted + 1
#     video.save()

#     if video.converted == 2:
#         os.remove(convert_video_name)