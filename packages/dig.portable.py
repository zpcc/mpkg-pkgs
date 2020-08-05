import time

from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'dig.portable'
    BIN = ['dig.exe']

    def _prepare(self):
        url = 'https://www.isc.org/bind/'
        item = [item for item in etree.HTML(GetPage(url)).xpath(
            '//*[@class="cursor-pointer"]') if item.text == 'Current-Stable'][0]
        self.ver = item.getprevious().text
        v = self.ver.split('.')[0]
        date = item.getnext().getnext().text
        self.date = time.strftime('%Y-%m-%d', time.strptime(date, '%B %Y'))
        self.log = f'https://downloads.isc.org/isc/bind{v}/{self.ver}/RELEASE-NOTES-bind-{self.ver}.html'
        self.link = {
            '64bit': f'https://downloads.isc.org/isc/bind{v}/{self.ver}/BIND{self.ver}.x64.zip'}
