from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'git'

    def _prepare(self):
        data = self.data
        data.args = '/sp- /verysilent /norestart'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/git-for-windows/git/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1]
        for link in links:
            if link.endswith('-64-bit.exe'):
                data.arch['64bit'] = link
            elif link.endswith('-32-bit.exe'):
                data.arch['32bit'] = link
