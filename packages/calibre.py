from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import Search


class Package(Soft):
    ID = 'calibre'

    def _prepare(self):
        data = self.data
        data.args = '/quiet'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/kovidgoyal/calibre/releases/latest'
        header, _, data.date = parser(url)
        data.changelog = 'https://calibre-ebook.com/whats-new'
        data.ver = header.split(' ')[-1]
        arch = {'32bit': 'https://download.calibre-ebook.com/{ver}/calibre-{ver}.msi',
                '64bit': 'https://download.calibre-ebook.com/{ver}/calibre-64bit-{ver}.msi'}
        data.arch = Search(links=arch, ver=data.ver)
