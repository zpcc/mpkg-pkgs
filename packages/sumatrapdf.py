from mpkg.common import Soft
from mpkg.utils import GetPage
from lxml import etree


class Package(Soft):
    ID = 'sumatrapdf'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        # https://github.com/sumatrapdfreader/sumatrapdf/releases/latest
        data.changelog = 'https://www.sumatrapdfreader.org/docs/Version-history.html'
        url = 'https://www.sumatrapdfreader.org/download-free-pdf-viewer.html'
        links = [x.values()[0]
                 for x in etree.HTML(GetPage(url)).xpath('//table//a')]
        for link in links:
            if link.startswith('/'):
                link = 'https://www.sumatrapdfreader.org' + link
            if link.endswith('.exe'):
                if link.endswith('-64-install.exe'):
                    data.arch['64bit'] = link
                    data.ver = link.split(
                        'SumatraPDF-')[1].split('-64-install.exe')[0]
                else:
                    data.arch['32bit'] = link
