"""
Youtube video downloader.

Reference:
1) https://stackoverflow.com/questions/40713268/download-youtube-video-using-python
2) https://github.com/nficano/pytube
"""
import os
import begin
import base64
from pytube import YouTube

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_PATH = os.path.join(root, "media")
ENCODING = "utf-8"


@begin.start
def run(url=None, path=DEFAULT_PATH, prefix="video"):
    """ Main Routine. """
    if not url or not isinstance(url, str):
        raise ValueError("Invalid URL.")
    if not os.path.isdir(path):
        raise RuntimeError("Invalid directory: {}.".format(path))
    y = YouTube(url)
    y = y.streams
    y = y.filter(subtype='mp4')
    y = y.filter(progressive=True)
    y = y.order_by('resolution').desc()
    y = y.first()
    filename = y.default_filename
    filename = base64.b64encode(filename.encode(ENCODING))
    filename = filename.decode(ENCODING)
    filename = filename.replace("=", "")
    filename = filename[:5]
    name = "{}_{}".format(prefix, filename)
    print(name + ".mp4")
    y = y.download(path, filename=name)
