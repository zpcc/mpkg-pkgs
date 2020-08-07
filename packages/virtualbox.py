from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'virtualbox'

    def _prepare(self):
        data = self.data
        url = 'https://www.virtualbox.org/wiki/Downloads'
        links = etree.HTML(GetPage(url)).xpath('//*[@class="ext-link"]')
        link = [link for link in links if list(
            link.itertext())[1] == 'Windows hosts'][0]
        data.arch = {'64bit': link.values()[1]}
        data.changelog = 'https://www.virtualbox.org/wiki/Changelog'
        data.ver = data.arch['64bit'].split('/virtualbox/')[1].split('/')[0]
