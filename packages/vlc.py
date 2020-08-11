from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'vlc'

    def _prepare(self):
        data = self.data
        arch = {'32bit': 'https://get.videolan.org/vlc/last/win32/vlc-{ver}-win32.exe',
                '64bit': 'https://get.videolan.org/vlc/last/win64/vlc-{ver}-win64.exe'}
        url = 'https://get.videolan.org/vlc/last/win64/'
        data.ver = Search(url, 'vlc-([\\d.]+)-win64.exe')
        data.arch = Search(links=arch, ver=data.ver)
        for k, v in data.arch.items():
            data.sha256[k] = Search(v, sumurl=v+'.sha256')
