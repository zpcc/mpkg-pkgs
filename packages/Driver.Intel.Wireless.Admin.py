import time
from urllib.parse import unquote

from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


def getIntelDrivers(u) -> list:
    page = etree.HTML(GetPage(u))
    u = [x.xpath('.//a')[0].values()[1]
         for x in page.xpath('//*[@class="download-file"]')]
    drivers = [unquote(x).split('httpDown=')[::-1][0] for x in u]
    version = page.xpath('//*[@class="version"]/span[2]')[0].text.strip()
    date = page.xpath('//*[@class="date"]/span[2]')[0].text.strip()
    date = time.strftime('%Y-%m-%d', time.strptime(date, '%m/%d/%Y'))
    return drivers, version, date


class Package(Soft):
    ID = 'IntelWirelessDriver.admin'

    def _prepare(self):
        data = self.data
        page = GetPage(
            'https://www.intel.com/content/www/us/en/support/articles/000017246/network-and-i-o/wireless-networking.html')
        tmp = [x for x in etree.HTML(page).xpath('//a')
               if b'Download Here' in etree.tostring(x)]
        if len(tmp) == 1:
            url = tmp[0].values()[0]
            data.changelog = url
            drivers, version, date = getIntelDrivers(url)
            data.links = sorted(drivers, reverse=True)
            data.date = date
            data.ver = version
        else:
            print('IntelWifi(Soft) parsing error')
