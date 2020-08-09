import json
from functools import lru_cache
from urllib.parse import unquote

from lxml import etree
from mpkg.common import Driver
from mpkg.utils import GetPage


@lru_cache()
def getIntelList(URL) -> list:
    # ['英特尔®显卡-Windows® 10 DCH 驱动程序', '驱动程序', ['Windows 10，64 位*'], '27.20.100.8280', '05-29-2020', '/zh-cn/download/29616/-Windows-10-DCH-']
    u = URL.split('/product/')
    u = u[0] + '/json/pageresults?pageNumber=2&productId=' + u[1]
    # u = u[0] + '/json/pageresults?productId=' + u[1]
    r = json.loads(GetPage(u))
    return [[x['Title'], x['DownloadType'], x['OperatingSystemSet'], x['Version'], x['PublishDateMMDDYYYY'], x['FullDescriptionUrl']] for x in r['ResultsForDisplay']]


def getIntelDrivers(u) -> list:
    r = GetPage(u)
    u = [x.xpath('.//a')[0].values()[1]
         for x in etree.HTML(r).xpath('//*[@class="download-file"]')]
    drivers = [unquote(x).split('httpDown=')[::-1][0] for x in u]
    return drivers


class Package(Driver):
    ID = 'IntelDriver'
    isMultiple = True

    def __init__(self):
        super().__init__()
        self.kw = self.getconfig('driverKeyword')

    def config(self):
        super().config()
        self.setconfig('driverKeyword')

    def _prepare(self):
        if not self.url:
            return
        data = self.data
        L = getIntelList(self.url)
        item = sorted([x for x in L if self.kw in x[0]],
                      key=lambda x: x[3], reverse=True)[0]
        date = item[4].split('-')
        data.date = '-'.join([date[-1]]+date[:-1])
        data.ver = item[3]
        url = 'https://downloadcenter.intel.com'+item[-1]
        data.changelog = url
        data.links = getIntelDrivers(url)
