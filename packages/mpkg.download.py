from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'mpkg.download'

    def _prepare(self):
        data = self.data
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/mpkg-project/mpkg/releases/latest'
        header, links, data.date = parser(url)
        data.ver = header.split('v')[-1]
        for link in links:
            if link.endswith('-win64.zip'):
                data.arch['64bit'] = link
            elif link.endswith('-win32.zip'):
                data.arch['32bit'] = link
