from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'wget'
    BIN = ['wget.exe']

    def _prepare(self):
        links = {'32bit': 'https://eternallybored.org/misc/wget/releases/wget-{ver}-win32.zip',
                 '64bit': 'https://eternallybored.org/misc/wget/releases/wget-{ver}-win64.zip'}
        url = 'https://eternallybored.org/misc/wget'
        regex = '<title>GNU Wget ([\\d.]+) for Windows'
        self.log = 'https://eternallybored.org/misc/wget'
        self.ver = Search(url, regex)
        self.link = Search(links=links, ver=self.ver)
