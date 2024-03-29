from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'wget'

    def _prepare(self):
        data = self.data
        data.bin = ['wget.exe']
        links = {'32bit': 'https://eternallybored.org/misc/wget/releases/wget-{ver}-win32.zip',
                 '64bit': 'https://eternallybored.org/misc/wget/releases/wget-{ver}-win64.zip'}
        url = 'https://eternallybored.org/misc/wget/releases/?C=M;O=D'
        regex = '>wget-([\\d.-]+)-win64\\.zip</a>'
        data.changelog = 'https://eternallybored.org/misc/wget'
        data.ver = Search(url, regex)
        data.arch = Search(links=links, ver=data.ver)
