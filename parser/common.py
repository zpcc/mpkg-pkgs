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
            result = 'https://downloads.sourceforge.net/project/' + \
                project[:-9].replace('/files/', '/')
            return result
        else:
            # input: https://sourceforge.net/projects/sevenzip/files/7-Zip/
            # output: [('19.00', '2019-02-22'), ('18.06', '2018-12-30')]
            #items = re.findall('net\.sf\.files = (.*);', GetPage(url))[0]
            folers = etree.HTML(GetPage(url)).xpath('//*[@class="folder "]')
            files = etree.HTML(GetPage(url)).xpath('//*[@class="file "]')
            result = [(item.xpath('.//span')[0].text,
                       item.xpath('.//abbr')[0].text) for item in (folers+files)]
            return result

    @staticmethod
    def github(url: str):
        # input: https://github.com/git-for-windows/git/releases/latest
        # output: ('Git for Windows 2.27.0', ['https://github.com/git-for-wind...], '2020-06-01')
        page = etree.HTML(GetPage(url))
        #release=page.xpath('//div[contains(@class, "release-main-section")]')[0]
        header = page.xpath('//*[@class="release-header"]')[0]
        text = header.xpath('./div/div/a')[0].text
        date = header.xpath('.//relative-time')[0].values()[0][:10]
        assests = page.xpath(
            '//*[@class="Box Box--condensed mt-3"]/div')[0].xpath('.//div')
        links = ['https://github.com' +
                 item.xpath('./a')[0].values()[0] for item in assests]
        return text, links, date

    @staticmethod
    def launchpad(url: str):
        if re.match('https?://launchpad.net/.*/trunk', url):
            # input: https://launchpad.net/veracrypt/trunk
            # output: [('VeraCrypt 1.24', 'https://launc.../+milestone/1.24', '2020-03-10')...]
            page = etree.HTML(GetPage(url))
            items = [item.xpath('.//td') for item in page.xpath(
                '//*[@id="milestone-rows"]')[0].xpath('.//tr')]
            items = [(item[0].getchildren()[1].text, 'https://launchpad.net' +
                      item[0].getchildren()[1].values()[0],
                      items[0][2].getchildren()[0].values()[0][:10]) for item in items]
            return items
        elif re.match('https?://launchpad.net/.*/\\+milestone/.*', url):
            # input: https://launchpad.net/veracrypt/+milestone/1.24-update6
            # output: ['https://launch...ypt-1.24-Update6-sha512sum.txt', 'https://launchp...sum.txt']
            page = etree.HTML(GetPage(url))
            items = [item.xpath('.//strong')[0] for item in page.xpath(
                '//*[@id="downloads"]')[0].xpath('.//tbody//tr')]
            return [dict(item.getchildren()[0].items())['href'] for item in items]
