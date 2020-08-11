from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import SearchSum


class Package(Soft):
    ID = 'notepadplusplus'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/notepad-plus-plus/notepad-plus-plus/releases'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1]
        for link in links:
            if link.endswith('.x64.exe'):
                data.arch['64bit'] = link
            elif link.endswith('.exe'):
                data.arch['32bit'] = link
        data.sha256 = SearchSum(data.arch, url)
