from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import Search


class Package(Soft):
    ID = 'exa'

    def _prepare(self):
        data = self.data
        data.bin = ['exa.exe']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/zpcc/mpkg-pkgs-selfbuilds/releases/tag/220306-2'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1][1:]
        for link in links:
            if link.endswith('-x86_64-msvc.zip'):
                data.arch['64bit'] = link
            elif link.endswith('-i686-msvc.zip'):
                data.arch['32bit'] = link
        data.sha256 = Search(data.arch, sumurl=url.replace(
            '/tag/', '/download/')+'/SHA256SUMS')
