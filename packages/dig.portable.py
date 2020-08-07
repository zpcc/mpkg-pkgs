import time

from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'dig.portable'

    def _prepare(self):
        data = self.data
        data.bin = ['dig.exe']
        url = 'https://www.isc.org/bind/'
        item = [item for item in etree.HTML(GetPage(url)).xpath(
            '//*[@class="cursor-pointer"]') if item.text == 'Current-Stable'][0]
        data.ver = item.getprevious().text
        v = data.ver.split('.')[0]
        date = item.getnext().getnext().text
        data.date = time.strftime('%Y-%m-%d', time.strptime(date, '%B %Y'))
        data.changelog = f'https://downloads.isc.org/isc/bind{v}/{data.ver}/RELEASE-NOTES-bind-{data.ver}.html'
        data.arch = {
            '64bit': f'https://downloads.isc.org/isc/bind{v}/{data.ver}/BIND{data.ver}.x64.zip'}
