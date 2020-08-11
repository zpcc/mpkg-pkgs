import time

from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'quiterss.portable'

    def _prepare(self):
        data = self.data
        data.bin = ['MPKGLNK||QuiteRSS.exe']
        url = 'https://quiterss.org/en/download'
        item = [item for item in etree.HTML(GetPage(url)).xpath(
            '//*[@class="field-items"]//p') if item.xpath('.//a')[0].text.endswith('Portable Windows')][0]
        texts = list(item.itertext())
        data.ver = texts[0].split(' ')[1]
        date = texts[-1].split('|')[0].strip()
        data.date = time.strftime('%Y-%m-%d', time.strptime(date, '%d.%m.%Y'))
        data.changelog = 'https://quiterss.org/en/history'
        data.links = [
            f'https://quiterss.org/files/{data.ver}_/QuiteRSS-{data.ver}.zip']
