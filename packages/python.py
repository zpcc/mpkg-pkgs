from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'python'

    def _prepare(self):
        data = self.data
        links = {'32bit': 'https://www.python.org/ftp/python/{ver}/python-{ver}.exe',
                 '64bit': 'https://www.python.org/ftp/python/{ver}/python-{ver}-amd64.exe'}
        url = 'https://www.python.org/'
        data.ver = Search(url, 'Latest: .*Python ([\\d\\.]+)')
        data.changelog = f'https://docs.python.org/release/{data.ver}/whatsnew/changelog.html#changelog'
        data.arch = Search(links=links, ver=data.ver)
