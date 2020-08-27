from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import Search


class Package(Soft):
    ID = 'brave'

    def _prepare(self):
        data = self.data
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/brave/brave-browser/raw/master/CHANGELOG_DESKTOP.md'
        ver = Search(url, r'(?m)^## \[([\d.]*)\]')
        _, links, data.date = parser(
            f'https://github.com/brave/brave-browser/releases/tag/v{ver}')
        for link in links:
            if link.endswith('BraveBrowserStandaloneSilentSetup.exe'):
                data.arch['64bit'] = link
            elif link.endswith('BraveBrowserStandaloneSilentSetup32.exe'):
                data.arch['32bit'] = link
