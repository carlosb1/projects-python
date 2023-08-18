
import ffmpeg
from pydub import silence
from pydub import AudioSegment 
import logging


def delete_silent_file(input_file, output_file):
    logger = logging.getLogger(__name__)
    probe = ffmpeg.probe(input_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    duration = float(video_stream['duration'])
    # number of  frames
    nb_frames = float(video_stream['nb_frames'])
    fps = nb_frames / duration
    logger.info("width: "+str(width) + " height: "+str(height) + "duration: "+str(duration) + "secs  nb_frames: "+str(nb_frames)+ " fps: "+str(fps))
    #Search silence parts
    song = AudioSegment.from_file(input_file)
    chunks_nosilent_frames = silence.detect_nonsilent(song)

    # iterate for chunks of the video with silence
    clips = []
    for [start_millisec, stop_millisec] in chunks_nosilent_frames:
        start_sec = start_millisec / 1000.
        stop_sec = stop_millisec / 1000.
        time_in_secs = stop_sec - start_sec
        clip = ffmpeg.input(input_file, ss=start_sec, t=time_in_secs)
        v = clip.video
        a = clip.audio
        clips.append(v)
        clips.append(a)

    # join all the parts
    concatenated =ffmpeg.concat(*clips, v=1, a=1)
    result = concatenated.output(output_file)
    result.run()
