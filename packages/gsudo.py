from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'gsudo'

    def _prepare(self):
        data = self.data
        data.bin = [['gsudo.exe', 'sudo']]
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/gerardog/gsudo/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1][1:]
        for link in links:
            if link.endswith('.zip') and link.split('/')[-1].startswith('gsudo'):
                data.links = [link]
                data.sha256 = [GetPage(link+'.sha256').strip()]
