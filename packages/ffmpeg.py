from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'ffmpeg'

    def _prepare(self):
        data = self.data
        data.bin = [r'bin\ffmpeg.exe', r'bin\ffplay.exe', r'bin\ffprobe.exe']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-github'
        header, links, data.date = parser(url)
        data.ver = header.split(' ')[1]
        data.changelog = 'https://ffmpeg.org/index.html#news'
        # 'ffmpeg-([\\d.-]+)-full_build-shared.(zip|7z)</a>'
        link = [link for link in links if 'full_build-shared.7z' in link][0]
        data.arch = {'64bit': link}
        data.sha256 = {'64bit': GetPage(
            'https://www.gyan.dev/ffmpeg/builds/sha256-release-full-shared')}
