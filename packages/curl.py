from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'curl'

    def _prepare(self):
        data = self.data
        data.bin = ['curl.exe']
        links = {'32bit': 'https://curl.haxx.se/windows/dl-{ver}/curl-{ver}-win32-mingw.zip',
                 '64bit': 'https://curl.haxx.se/windows/dl-{ver}/curl-{ver}-win64-mingw.zip'}
        url = 'https://curl.haxx.se/windows/'
        data.changelog = 'https://curl.haxx.se/changes.html'
        data.ver = Search(url, 'Build<\\/b>:\\s+([\\d._]+)')
        data.arch = Search(links=links, ver=data.ver)
        data.date = Search(url, 'Date<\\/b>:\\s+([\\d._|-]+)')
