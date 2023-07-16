from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'wireshark'

    def _prepare(self):
        data = self.data
        data.args = '/S /quicklaunchicon=no'
        links = {
            '64bit': 'https://www.wireshark.org/download/win64/Wireshark-win64-{ver}.exe'}
        url = 'https://www.wireshark.org/download.html'
        data.ver = Search(url, 'Stable Release: ([\\d.]+)')
        data.changelog = f'https://www.wireshark.org/docs/relnotes/wireshark-{data.ver}.html'
        data.arch = Search(links=links, ver=data.ver)
        for k, v in data.arch.items():
            fn = v.split('/')[-1]
            data.sha256[k] = Search(
                f'https://www.wireshark.org/download/SIGNATURES-{data.ver}.txt', f'SHA2?-?256\\({fn}\\)=\\s*(\\w+)')
