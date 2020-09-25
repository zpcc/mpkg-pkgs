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
        text = Search(
            url, 'ffmpeg-([\\d.-]+)-full_build.zip</a>', reverse=True)
        data.ver = text.split('-')[0]
        data.arch = Search(links=links, ver=text)
        data.date = '-'.join(text.split('-')[1:])
