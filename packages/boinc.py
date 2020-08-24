from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'boinc'

    def _prepare(self):
        data = self.data
        url = 'https://boinc.berkeley.edu/download.php'
        link = etree.HTML(GetPage(url)).xpath(
            '//*[@class="btn btn-info"]')[0].values()[0]
        data.arch = {'64bit': link}
        data.changelog = 'https://boinc.berkeley.edu/wiki/Release_Notes'
        data.ver = link.split('/')[-1].split('_')[1]
