from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'mpc-hc-fork'

    def _prepare(self):
        data = self.data
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/clsid2/mpc-hc/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1]
        for link in links:
            if link.endswith('.x64.exe'):
                data.arch['64bit'] = link
            elif link.endswith('.x86.exe'):
                data.arch['32bit'] = link
