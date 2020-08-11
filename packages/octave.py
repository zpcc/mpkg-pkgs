from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'octave'

    def _prepare(self):
        data = self.data
        arch = {'32bit': 'https://ftp.gnu.org/gnu/octave/windows/octave-{ver}-w32-installer.exe',
                '64bit': 'https://ftp.gnu.org/gnu/octave/windows/octave-{ver}-w64-installer.exe'}
        url = 'https://ftp.gnu.org/gnu/octave/windows/'
        data.ver = Search(
            url, 'octave-([\\d._]+)-w64-installer.exe', reverse=True)
        data.arch = Search(links=arch, ver=data.ver)
        data.changelog = 'https://www.gnu.org/software/octave/news.html'
