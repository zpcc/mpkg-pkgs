from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'wget'
    BIN = ['wget.exe']

    def _prepare(self):
        data = self.data
        data.bin = ['wget.exe']
        links = {'32bit': 'https://eternallybored.org/misc/wget/releases/wget-{ver}-win32.zip',
                 '64bit': 'https://eternallybored.org/misc/wget/releases/wget-{ver}-win64.zip'}
        url = 'https://eternallybored.org/misc/wget'
        regex = '<title>GNU Wget ([\\d.]+) for Windows'
        data.changelog = 'https://eternallybored.org/misc/wget'
        data.ver = Search(url, regex)
        data.arch = Search(links=links, ver=data.ver)
