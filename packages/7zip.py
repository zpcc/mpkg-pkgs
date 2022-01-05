from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = '7zip'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        data.changelog = 'https://www.7-zip.org/history.txt'
        items = Search('https://www.7-zip.org/download.html',
                       f'Download 7-Zip ([\\d.]+ \\([0-9-]*\\))').split(' ')
        data.ver = items[0]
        data.date = items[1][1:-1]
        v = data.ver.replace('.', '')
        data.arch = {'32bit': f'https://www.7-zip.org/a/7z{v}.exe',
                     '64bit': f'https://www.7-zip.org/a/7z{v}-x64.exe'}
