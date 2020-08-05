import time

from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'ffmpeg'
    BIN = [r'bin\ffmpeg.exe', r'bin\ffplay.exe', r'bin\ffprobe.exe']

    def _prepare(self):
        links = {'32bit': 'https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-{ver}-win32-static.zip',
                 '64bit': 'https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-{ver}-win64-static.zip'}
        url = 'https://ffmpeg.zeranoe.com/builds/win64/static'
        self.log = 'https://ffmpeg.org/index.html#news'
        self.ver = Search(
            url, 'ffmpeg-([\\d.]+)-win64-static\\.zip</a>', reverse=True)
        self.link = Search(links=links, ver=self.ver)
        date = Search(
            url, 'ffmpeg-[\\d.]+-win64-static\\.zip</a>[ ]+(\\S*)', reverse=True)
        self.date = time.strftime('%Y-%m-%d', time.strptime(date, '%d-%b-%Y'))
