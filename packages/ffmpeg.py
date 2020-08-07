import time

from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'ffmpeg'

    def _prepare(self):
        data = self.data
        data.bin = [r'bin\ffmpeg.exe', r'bin\ffplay.exe', r'bin\ffprobe.exe']
        links = {'32bit': 'https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-{ver}-win32-static.zip',
                 '64bit': 'https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-{ver}-win64-static.zip'}
        url = 'https://ffmpeg.zeranoe.com/builds/win64/static'
        data.changelog = 'https://ffmpeg.org/index.html#news'
        data.ver = Search(
            url, 'ffmpeg-([\\d.]+)-win64-static\\.zip</a>', reverse=True)
        data.arch = Search(links=links, ver=data.ver)
        date = Search(
            url, 'ffmpeg-[\\d.]+-win64-static\\.zip</a>[ ]+(\\S*)', reverse=True)
        data.date = time.strftime('%Y-%m-%d', time.strptime(date, '%d-%b-%Y'))
