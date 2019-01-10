"""
Video subclip extractor.

Reference:
1) https://github.com/Zulko/moviepy
2) https://stackoverflow.com/questions/37317140/cutting-out-a-portion-of-video-python
3) https://zulko.github.io/moviepy/getting_started/videoclips.html
"""

import os
import begin

from moviepy.editor import VideoFileClip

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_PATH = os.path.join(root, "media")


@begin.start
def run(name=None, path=DEFAULT_PATH, start=0, end=10):
    """ Main Routine. """
    if not name or not isinstance(name, str):
        raise ValueError("Invalid name.")
    if not os.path.isdir(path):
        raise RuntimeError("Invalid directory: {}.".format(path))
    source = os.path.join(path, name)
    if not os.path.isfile(source):
        raise RuntimeError("Invalid source file: {}.".format(source))
    start = float(start)
    end = float(end)
    if start < 0 or end <= start:
        raise ValueError("Invalid start and end time: {}-{}".format(start, end))
    clip = VideoFileClip(source)
    subclip = clip.subclip(start, end)
    filename = name.split(".")[0]
    extension = name.split(".")[1]
    new_name = "{}_subclip_{}_{}.{}".format(filename, int(start), int(end), extension)
    target = os.path.join(path, new_name)
    subclip.write_videofile(target)
    print(new_name)
