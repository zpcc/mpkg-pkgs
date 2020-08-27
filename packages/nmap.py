from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'nmap'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        links = ['https://nmap.org/dist/nmap-{ver}-setup.exe']
        url = 'https://nmap.org/download.html'
        data.changelog = 'https://nmap.org/changelog.html'
        data.ver = Search(url, 'nmap-([\\d.]+)-setup.exe')
        data.links = Search(links=links, ver=data.ver)
