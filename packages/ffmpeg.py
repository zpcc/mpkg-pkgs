import time

from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'ffmpeg'

    def _prepare(self):
        data = self.data
        data.bin = [r'bin\ffmpeg.exe', r'bin\ffplay.exe', r'bin\ffprobe.exe']
        links = {
            '64bit': 'https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-{ver}-full_build.zip'}
        url = 'https://www.gyan.dev/ffmpeg/builds/packages/'
        data.changelog = 'https://ffmpeg.org/index.html#news'
        data.ver = Search(
            url, 'ffmpeg-([\\d.]+)-full_build.zip</a>', reverse=True)
        data.arch = Search(links=links, ver=data.ver)
        data.date = Search(
            url, 'ffmpeg-[\\d.]+-full_build.zip</a>[ ]+(\\S*)', reverse=True)
