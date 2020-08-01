from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'virtualbox'

    def _prepare(self):
        url = 'https://www.virtualbox.org/wiki/Downloads'
        links = etree.HTML(GetPage(url)).xpath('//*[@class="ext-link"]')
        link = [link for link in links if list(
            link.itertext())[1] == 'Windows hosts'][0]
        self.link = {'64bit': link.values()[1]}
        self.log = 'https://www.virtualbox.org/wiki/Changelog'
        self.ver = self.link['64bit'].split('/virtualbox/')[1].split('/')[0]
