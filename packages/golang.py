from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'golang'

    def _prepare(self):
        data = self.data
        data.changelog = 'https://golang.org/doc/devel/release.html'
        url = 'https://golang.org/dl/'
        L = etree.HTML(GetPage(url)).xpath(
            '//*[@class="downloadtable"]')[0].xpath('.//tr')
        table = [[''.join(list(y.itertext()))
                  for y in x.xpath('.//td')] for x in L]
        for item in table:
            if len(item) == 6 and item[0].endswith('.windows-amd64.msi'):
                data.sha256 = {'64bit': item[5]}
                data.arch = {'64bit': url+item[0]}
                data.ver = item[0].split('.windows-amd64.msi')[0][2:]
