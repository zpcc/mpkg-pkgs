from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'curl'

    def _prepare(self):
        data = self.data
        data.bin = ['bin\\curl.exe']
        links = {'32bit': 'https://curl.se/windows/dl-{ver}/curl-{ver}-win32-mingw.zip',
                 '64bit': 'https://curl.se/windows/dl-{ver}/curl-{ver}-win64-mingw.zip'}
        url = 'https://curl.se/windows/'
        data.changelog = 'https://curl.se/changes.html'
        data.ver = Search(url, 'Build<\\/b>:\\s+([\\d._]+)')
        data.arch = Search(links=links, ver=data.ver)
        data.date = Search(url, 'Date<\\/b>:\\s+([\\d._|-]+)')
        u = f'https://curl.se/windows/dl-{data.ver}/hashes.txt'
        for k, v in data.arch.items():
            fn = v.split('/')[-1]
            data.sha256[k] = Search(u, f'SHA256\\({fn}\\)=\\s+(\\w+)')
