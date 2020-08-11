from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'iperf3'

    def _prepare(self):
        data = self.data
        data.bin = ['iperf3.exe']
        arch = {'32bit': 'https://iperf.fr/download/windows/iperf-{ver}-win32.zip',
                '64bit': 'https://iperf.fr/download/windows/iperf-{ver}-win64.zip'}
        url = 'https://iperf.fr/iperf-download.php'
        data.ver = Search(url, 'iPerf ([\\d.]+)<\\/a>')
        data.arch = Search(links=arch, ver=data.ver)
        data.sha256 = Search(
            data.arch, sumurl='https://iperf.fr/download/windows/sha256sum.txt')
