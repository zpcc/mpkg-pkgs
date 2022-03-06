from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'binocle'

    def _prepare(self):
        data = self.data
        data.bin = ['binocle.exe']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/sharkdp/binocle/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1][1:]
        for link in links:
            if link.endswith('-x86_64-pc-windows-msvc.zip'):
                data.arch['64bit'] = link
            elif link.endswith('-i686-pc-windows-msvc.zip'):
                data.arch['32bit'] = link
