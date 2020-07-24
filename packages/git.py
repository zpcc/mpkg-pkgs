from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'git'
    SilentArgs = '/sp- /verysilent /norestart'

    def _prepare(self):
        parser = Load(
            'https://github.com/zpcc/mpkg-pkgs/raw/master/parser/common.py')[0][0].github
        url = 'https://github.com/git-for-windows/git/releases/latest'
        header, links, self.date = parser(url)
        self.log = url
        self.ver = header.split(' ')[-1]
        for link in links:
            if link.endswith('-64-bit.exe'):
                self.link['64bit'] = link
            elif link.endswith('-32-bit.exe'):
                self.link['32bit'] = link
