from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'vlc'

    def _prepare(self):
        data = self.data
        arch = {'32bit': 'https://download.videolan.org/pub/videolan/vlc/{ver}/win32/vlc-{ver}-win32.exe',
                '64bit': 'https://download.videolan.org/pub/videolan/vlc/{ver}/win64/vlc-{ver}-win64.exe'}
        url = 'https://www.videolan.org/vlc/download-windows.html'
        data.ver = Search(url, 'Version.*\\s+([\\d.]+)</span>')
        data.arch = Search(links=arch, ver=data.ver)
        for k, v in data.arch.items():
            data.sha256[k] = Search(v, sumurl=v+'.sha256')
        data.arch = arch
