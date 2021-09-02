import json
from functools import lru_cache

from lxml import etree
from mpkg.common import Driver
from mpkg.utils import GetPage, Selected


@lru_cache()
def getDriverList(URL) -> list:
    # init: mpkg load Driver.Intel.py --config
    # ['英特尔®显卡 – Windows® 10 和 Windows 11* DCH 驱动程序', '30.0.100.9805', '5/29/2020', 'https://www.intel.com/content/www/cn/zh/download/19344']
    data = GetPage(URL).split('var upeDownloads = ')[1].split('\n')[0][:-1]
    L = [v for k, v in json.loads(data).items() if k.isdigit()]
    return [[x['name'], x['version'], x['lastUpdated'], x['url']] for x in L]


def getDriverUrls(u) -> list:
    r = GetPage(u)
    return [x.get('data-href')
            for x in etree.HTML(r).xpath('//*[@class="dc-page-available-downloads-hero-button"]/button')]


class Package(Driver):
    ID = 'IntelDriver'
    isMultiple = True

    def __init__(self):
        super().__init__()
        self.kw = self.getconfig('driverKeyword')

    def config(self):
        super().config()
        L = [x[0] for x in getDriverList(self.getconfig('url'))]
        print('please select the driver you need')
        self.setconfig('driverKeyword', Selected(L)[0])

    def _prepare(self):
        if not self.url:
            return
        data = self.data
        L = getDriverList(self.url)
        item = [x for x in L if self.kw == x[0]][0]
        date = item[2].split('/')
        data.date = '-'.join([date[-1]]+date[:-1])
        data.ver = item[1]
        url = item[-1]
        data.changelog = url
        data.links = getDriverUrls(url)
