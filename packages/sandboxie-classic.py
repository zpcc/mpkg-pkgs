from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'sandboxie'

    def _prepare(self):
        data = self.data
        url = 'https://github.com/sandboxie-plus/Sandboxie/releases/latest'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1]
        for link in links:
            if 'Sandboxie-Classic-x64-' in link:
                data.arch['64bit'] = link
            elif 'Sandboxie-Classic-x86-' in link:
                data.arch['32bit'] = link
