from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'aria2'

    def _prepare(self):
        data = self.data
        data.bin = ['aria2c.exe']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/aria2/aria2/releases'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1]
        for link in links:
            if '-64bit-' in link:
                data.arch['64bit'] = link
            elif '-32bit-' in link:
                data.arch['32bit'] = link
