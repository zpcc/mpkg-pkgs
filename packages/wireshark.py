from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'wireshark'

    def _prepare(self):
        data = self.data
        data.args = '/S /quicklaunchicon=no'
        links = {'32bit': 'https://1.na.dl.wireshark.org/win32/Wireshark-win32-{ver}.exe',
                 '64bit': 'https://1.na.dl.wireshark.org/win64/Wireshark-win64-{ver}.exe'}
        url = 'https://www.wireshark.org/docs/relnotes/'
        data.ver = Search(url, 'Wireshark ([\\d.]+)')
        data.changelog = f'https://www.wireshark.org/docs/relnotes/wireshark-{data.ver}.html'
        data.arch = Search(links=links, ver=data.ver)
