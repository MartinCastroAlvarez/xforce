"""
Add logo to video.

Reference:
1) https://github.com/Zulko/moviepy/issues/127
"""

import os
import begin

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_PATH = os.path.join(root, "media")
LOGO_PATH = os.path.join(root, "logo")


@begin.start
def run(name=None, logo=None, path=DEFAULT_PATH, logo_path=LOGO_PATH, margin=25, size=120, opacity=0.75):
    """ Main Routine. """

    # Validate video file.
    if not name or not isinstance(name, str):
        raise ValueError("Invalid name.")
    if not os.path.isdir(path):
        raise RuntimeError("Invalid directory: {}.".format(path))
    source = os.path.join(path, name)
    if not os.path.isfile(source):
        raise RuntimeError("Invalid source file: {}.".format(source))

    # Validate logo file.
    if not logo or not isinstance(logo, str):
        raise ValueError("Invalid logo.")
    if not os.path.isdir(logo_path):
        raise RuntimeError("Invalid directory: {}.".format(logo_path))
    logo_source = os.path.join(logo_path, logo)
    if not os.path.isfile(source):
        raise RuntimeError("Invalid logo file: {}.".format(logo_source))

    # Validate size.
    size = int(size)
    if size <= 0:
        raise ValueError("Size must be positive.")

    # Validate opacity.
    opacity = float(opacity)
    if opacity < 0:
        raise ValueError("Opacity must be positive or zero.")
    if opacity > 1:
        raise ValueError("Opacity must be less or equal than 1.")

    # Validate margin.
    margin = int(margin)
    if margin < 0:
        raise ValueError("Margin must be positive or zero.")

    # Background movie Clip.
    clip = VideoFileClip(source)

    # Logo image clip.
    logo_clip = ImageClip(logo_source)
    logo_clip = logo_clip.set_duration(clip.duration)
    logo_clip = logo_clip.resize(height=size)
    logo_clip = logo_clip.set_opacity(opacity * 0.80)
    logo_clip = logo_clip.set_position([margin, margin])

    # Merge Layers.
    final = CompositeVideoClip([clip, logo_clip])

    # Save composite video.
    logo_name = logo.split(".")[0]
    filename = name.split(".")[0]
    extension = name.split(".")[1]
    new_name = "{}_logo_{}_{}_{}.{}".format(filename, logo_name, size, margin, extension)
    target = os.path.join(path, new_name)
    final.write_videofile(target)
    print(new_name)
