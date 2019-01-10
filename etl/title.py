"""
Add title to video.

Reference:
1) https://github.com/Zulko/moviepy/issues/127
"""

import os
import begin

from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_PATH = os.path.join(root, "media")


@begin.start
def run(name=None, path=DEFAULT_PATH, secondary="#181818",
        margin=25, size=120, opacity=0.75, text="@vida.python", primary="#EDEDED"):
    """ Main Routine. """

    # Validate video file.
    if not name or not isinstance(name, str):
        raise ValueError("Invalid name.")
    if not os.path.isdir(path):
        raise RuntimeError("Invalid directory: {}.".format(path))
    source = os.path.join(path, name)
    if not os.path.isfile(source):
        raise RuntimeError("Invalid source file: {}.".format(source))

    # Validate text.
    if not text or not isinstance(text, str):
        raise ValueError("Invalid text string.")
    if not primary or not isinstance(primary, str):
        raise ValueError("Invalid text primary color.")
    if not secondary or not isinstance(secondary, str):
        raise ValueError("Invalid text secondary color.")

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

    # Initialize layers.
    layers = []

    # Background movie Clip.
    clip = VideoFileClip(source)
    layers.append(clip)

    # Title text clip.
    grace = int(margin / 3)
    text_clip = TextClip(text, color=primary, font="Amiri-Bold", fontsize=size,
                         stroke_color=secondary, stroke_width=1)
    text_clip = text_clip.resize(width=size + grace * 2)
    text_clip = text_clip.set_duration(clip.duration)
    text_clip = text_clip.set_opacity(opacity)
    text_clip = text_clip.set_position([margin - grace, margin + size])
    layers.append(text_clip)

    # Merge Layers.
    final = CompositeVideoClip(layers)

    # Save composite video.
    filename = name.split(".")[0]
    extension = name.split(".")[1]
    new_name = "{}_title_{}_{}.{}".format(filename, size, margin, extension)
    target = os.path.join(path, new_name)
    final.write_videofile(target)
    print(new_name)
