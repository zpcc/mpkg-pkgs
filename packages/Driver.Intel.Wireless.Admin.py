import time
from urllib.parse import unquote

from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


def getIntelDrivers(u) -> list:
    r = GetPage(u)
    u = [x.xpath('.//a')[0].values()[1]
         for x in etree.HTML(r).xpath('//*[@class="download-file"]')]
    drivers = [unquote(x).split('httpDown=')[::-1][0] for x in u]
    return drivers


class Package(Soft):
    ID = 'IntelWirelessDriver.admin'

    def _prepare(self):
        page = GetPage(
            'https://www.intel.com/content/www/us/en/support/articles/000017246/network-and-i-o/wireless-networking.html')
        tmp = [x for x in etree.HTML(page).xpath('//p')
               if b'Last Reviewed' in etree.tostring(x)][0]
        date = list(tmp.itertext())[2].replace(' ', '').strip()
        self.date = time.strftime('%Y-%m-%d', time.strptime(date, '%m/%d/%Y'))
        tmp = [x for x in etree.HTML(page).xpath('//a')
               if b'Download Here' in etree.tostring(x)]
        if len(tmp) == 1:
            self.links = sorted(getIntelDrivers(
                tmp[0].values()[0]), reverse=True)
            for link in self.links:
                if link.endswith('_all.zip'):
                    self.ver = link.split('_all.zip')[0].split('_')[-1]
        else:
            print('IntelWifi(Soft) parsing error')
