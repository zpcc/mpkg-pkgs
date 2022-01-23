from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import Search


class Package(Soft):
    ID = 'tcping'

    def _prepare(self):
        data = self.data
        data.bin = ['tcping.exe']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/zpcc/tcping/releases/latest'
        v, links, data.date = parser(url)
        data.ver = v.replace('Release v', '')
        for link in links:
            if 'windows-amd64' in link:
                data.arch['64bit'] = link
            elif 'windows-386' in link:
                data.arch['32bit'] = link
