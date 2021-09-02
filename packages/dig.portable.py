import time

from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'dig.portable'

    def _prepare(self):
        data = self.data
        data.bin = ['dig.exe']
        url = 'https://downloads.isc.org/isc/bind9/'
        page = etree.HTML(GetPage(url))
        L = [x.text for x in page.xpath('//*[@class="indexcolname"]/a')]
        L = [x[:-1] for x in L if x.startswith('9.16')]
        data.ver = L[-1]
        date = page.xpath(f'//*[@href="{data.ver}/"]/..')[0].getnext().text
        data.date = date.split(' ')[0]
        data.changelog = f'https://downloads.isc.org/isc/bind9/{data.ver}/RELEASE-NOTES-bind-{data.ver}.html'
        data.arch = {
            '64bit': f'https://downloads.isc.org/isc/bind9/{data.ver}/BIND{data.ver}.x64.zip'}
