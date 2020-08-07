import time

from lxml import etree

from mpkg.common import Driver
from mpkg.utils import GetPage

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'


class Package(Driver):
    ID = 'NvidiaDriver'
    allowExtract = True

    def __init__(self):
        super().__init__()
        self.isStudio = bool(self.getconfig('isStudio'))

    def config(self):
        super().config()
        self.setconfig('isStudio',
                       input('only download Studio Driver ? (press enter means no, input 1 means yes): '))

    def _prepare(self):
        data = self.data
        r = GetPage(self.url, UA=UA)
        L = etree.HTML(r).xpath('//*[@id="driverList"]')
        if self.isStudio:
            L = [x for x in L if x.xpath(
                './/a')[0].text == 'NVIDIA Studio Driver']
        else:
            L = [x for x in L if x.xpath(
                './/a')[0].text != 'NVIDIA Studio Driver']
        r = L[0].xpath('.//td')
        data.date = time.strftime(
            '%Y-%m-%d', time.strptime(r[3].text, '%B %d, %Y'))
        data.ver = r[2].text
        data.changelog = f'https://us.download.nvidia.com/Windows/{data.ver}/{data.ver}-win10-win8-win7-release-notes.pdf'
        result = 'https:'+r[1].xpath('.//a')[0].values()[0]
        link = etree.HTML(GetPage(result, UA=UA)).xpath(
            '//*[@id="lnkDwnldBtn"]')[0].values()[0]
        data.arch = {
            '64bit': 'https://us.download.nvidia.com'+link.split('confirmation.php?url=')[1].split('&')[0]}
