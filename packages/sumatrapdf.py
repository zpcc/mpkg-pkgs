from mpkg.common import Soft
from mpkg.utils import GetPage
from lxml import etree


class Package(Soft):
    ID = 'sumatrapdf'
    SilentArgs = '/S'

    def _prepare(self):
        # https://github.com/sumatrapdfreader/sumatrapdf/releases/latest
        self.log = 'https://www.sumatrapdfreader.org/docs/Version-history.html'
        url = 'https://www.sumatrapdfreader.org/download-free-pdf-viewer.html'
        links = ['https://www.sumatrapdfreader.org'+x.values()[0]
                 for x in etree.HTML(GetPage(url)).xpath('//table//a')]
        for link in links:
            if link.endswith('.exe'):
                if link.endswith('-64-install.exe'):
                    self.link['64bit'] = link
                    self.ver = link.split(
                        'SumatraPDF-')[1].split('-64-install.exe')[0]
                else:
                    self.link['32bit'] = link
