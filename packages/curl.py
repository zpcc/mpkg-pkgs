from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'curl'
    BIN = ['curl.exe']

    def _prepare(self):
        links = {'32bit': 'https://curl.haxx.se/windows/dl-{ver}/curl-{ver}-win32-mingw.zip',
                 '64bit': 'https://curl.haxx.se/windows/dl-{ver}/curl-{ver}-win64-mingw.zip'}
        url = 'https://curl.haxx.se/windows/'
        self.log = 'https://curl.haxx.se/changes.html'
        self.ver = Search(url, 'Build<\\/b>:\\s+([\\d._]+)')
        self.link = Search(links=links, ver=self.ver)
        self.date = Search(url, 'Date<\\/b>:\\s+([\\d._|-]+)')
