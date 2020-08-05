from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'aria2'
    BIN = ['aria2c.exe']

    def _prepare(self):
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/aria2/aria2/releases'
        header, links, self.date = parser(url)
        self.log = url
        self.ver = header.split(' ')[-1]
        for link in links:
            if '-64bit-' in link:
                self.link['64bit'] = link
            elif '-32bit-' in link:
                self.link['32bit'] = link
