"""
Video fade in/out.

Reference:
1) https://zulko.github.io/moviepy/ref/videofx/moviepy.video.fx.all.fadein.html
2) https://zulko.github.io/moviepy/ref/videofx/moviepy.video.fx.all.fadeout.html
3) https://zulko.github.io/moviepy/ref/videofx/moviepy.audio.fx.all.audio_fadein.html
4) https://zulko.github.io/moviepy/ref/videofx/moviepy.audio.fx.all.audio_fadeout.html
"""

import os
import begin

from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import fadein, fadeout
from moviepy.audio.fx.all import audio_fadein, audio_fadeout

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_PATH = os.path.join(root, "media")


@begin.start
def run(name=None, path=DEFAULT_PATH, duration=0.4, red=24, green=24, blue=24):
    """ Main Routine. """
    if not name or not isinstance(name, str):
        raise ValueError("Invalid name.")
    if not os.path.isdir(path):
        raise RuntimeError("Invalid directory: {}.".format(path))
    source = os.path.join(path, name)
    if not os.path.isfile(source):
        raise RuntimeError("Invalid source file: {}.".format(source))
    duration = float(duration)
    if duration < 0:
        raise ValueError("Invalid duration time: {}".format(duration))
    red = int(red)
    blue = int(blue)
    green = int(green)
    if red < 0 or red > 255:
        raise ValueError("Invalid red: {}.".format(red))
    if blue < 0 or blue > 255:
        raise ValueError("Invalid blue: {}.".format(blue))
    if green < 0 or green > 255:
        raise ValueError("Invalid green: {}.".format(green))
    color = [red, green, blue]
    clip = VideoFileClip(source)
    clip = fadein(clip, duration=duration, initial_color=color)
    clip = fadeout(clip, duration=duration, final_color=color)
    clip = audio_fadein(clip, duration=duration)
    clip = audio_fadeout(clip, duration=duration)
    filename = name.split(".")[0]
    extension = name.split(".")[1]
    new_name = "{}_fade_{}.{}".format(filename, int(duration), extension)
    target = os.path.join(path, new_name)
    clip.write_videofile(target)
    print(new_name)
