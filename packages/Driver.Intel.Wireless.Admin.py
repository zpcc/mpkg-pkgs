import time
from urllib.parse import unquote

from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


def getIntelDrivers(u) -> list:
    page = etree.HTML(GetPage(u))
    drivers = [x.get('data-href')
               for x in page.xpath('//*[@class="dc-page-available-downloads-hero-button"]/button')]
    version = page.xpath(
        '//*[@class="dc-page-banner-actions-action__select-version"]/select/option[@selected="selected"]')[0].text.replace(' (Latest)', '')
    date = page.xpath(
        '//div[contains(@class, "dc-page-banner-actions-action-updated")]/span')[0].text.strip()
    date = time.strftime('%Y-%m-%d', time.strptime(date, '%m/%d/%Y'))
    return drivers, version, date


class Package(Soft):
    ID = 'IntelWirelessDriver.admin'

    def _prepare(self):
        data = self.data
        site = 'https://www.intel.com'
        page = GetPage(
            site+'/content/www/us/en/support/articles/000017246/network-and-i-o/wireless-networking.html')
        tmp = [x for x in etree.HTML(page).xpath('//a')
               if b'Download Here' in etree.tostring(x)]
        if len(tmp) == 1:
            url = tmp[0].values()[0]
            data.changelog = site+url
            drivers, version, date = getIntelDrivers(site+url)
            data.links = sorted(drivers, reverse=True)
            data.date = date
            data.ver = version
        else:
            print('IntelWifi(Soft) parsing error')
