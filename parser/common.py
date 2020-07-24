import json
import re

from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage


class Package(Soft):
    @staticmethod
    def sourceforge(url: str):
        if url.endswith('/download'):
            # input: https://sourceforge.net/projects/sevenzip/files/7-Zip/19.00/7z1900.exe/download
            # output: https://newcontinuum.dl.sourceforge.net/project/sevenzip/7-Zip/19.00/7z1900.exe
            project = re.findall(
                'https?://sourceforge.net/projects/(.*)', url)[0]
            result = 'https://newcontinuum.dl.sourceforge.net/project/' + \
                project[:-9].replace('/files/', '/')
            return result
        else:
            # output: [('19.00', '2019-02-22'), ('18.06', '2018-12-30')]
            #items = re.findall('net\.sf\.files = (.*);', GetPage(url))[0]
            folers = etree.HTML(GetPage(url)).xpath('//*[@class="folder "]')
            files = etree.HTML(GetPage(url)).xpath('//*[@class="file "]')
            result = [(item.xpath('.//span')[0].text,
                       item.xpath('.//abbr')[0].text) for item in (folers+files)]
            return result
