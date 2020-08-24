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
        data.ver, _, data.date = parser(url)
        arch = {'32bit': 'https://github.com/zpcc/tcping/releases/download/{ver}/tcping-windows-386-{ver}.zip',
                '64bit': 'https://github.com/zpcc/tcping/releases/download/{ver}/tcping-windows-amd64-{ver}.zip'}
        data.arch = Search(links=arch, ver=data.ver)
