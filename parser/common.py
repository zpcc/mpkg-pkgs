import json
import re

from lxml import etree
from mpkg.common import Soft, soft_data
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
                       item.xpath('.//abbr')[0].values()[0][:10]) for item in (folers+files)]
            return result

    @staticmethod
    def github(url: str, getall=False, regex='.*', raw=False):
        if getall:
            rels = [rel for rel in json.loads(GetPage(
                f'https://api.github.com/repos/{url}/releases')) if re.match(regex, rel['name'])]
            if raw:
                return rels
            return [(rel['name'], [asset['browser_download_url'] for asset in rel['assets']],
                     rel['published_at'][:10]) for rel in rels]
        # input: https://github.com/git-for-windows/git/releases/latest
        # output: ('Git for Windows 2.27.0', ['https://github.com/git-for-wind...], '2020-06-01')
        page = etree.HTML(GetPage(url))
        #release=page.xpath('//div[contains(@class, "release-main-section")]')[0]
        title = page.xpath('//*[@class="flex-1"]/h1')[0].text
        date = page.xpath('//*[@datetime]')[0].values()[0][:10]
        assests = page.xpath('//*[@class="Box Box--condensed mt-3"]//li')
        links = ['https://github.com' +
                 item.xpath('.//a')[0].values()[0] for item in assests]
        return title, links, date

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

    @staticmethod
    def scoop(url='', data='', getbin=False, getlnk=False, detail=True, scoop_rename=False):

        def rename(url):
            def str_rename(url):
                len_ = len(url.split('#/'))
                if len_ > 1:
                    return '#/'.join(url.split('#/')[:-1])
                else:
                    return url.split('#/')[0]
            if isinstance(url, str):
                return str_rename(url)
            elif isinstance(url, list):
                return [str_rename(item) for item in url]
            else:
                return url

        def get_bin(data):
            if getbin and data.get('bin'):
                if not isinstance(data['bin'], list):
                    return [data['bin']]
                return data['bin']
            else:
                return {}

        def get_lnk(data):
            def tolnk(list_):
                if len(list_) == 2:
                    list_ = list_+['']
                else:
                    list_[2] = ' '+list_[2]
                return f'MPKGLNK|{list_[1]}|{list_[0]}|{list_[2]}'
            lnk_list = data.get('shortcuts')
            if getlnk and lnk_list:
                return [tolnk(lnk) for lnk in lnk_list]
            else:
                return []

        soft = soft_data()
        if not data:
            data = json.loads(GetPage(url))
        else:
            data = json.loads(data)
        soft.id = url.split('/')[-1].split('.json')[0]
        if data.get('version'):
            soft.ver = data['version']
        if data.get('url'):
            url = data['url'] if scoop_rename else rename(data['url'])
            url = [url] if isinstance(url, str) else url
            soft.links = url
            if data.get('hash'):
                sha256 = [data['hash']] if isinstance(
                    data['hash'], str) else data['hash']
                soft.sha256 = sha256
            if get_bin(data):
                soft.bin = get_bin(data)
            if get_lnk(data) and not soft.bin:
                soft.bin = []
            for lnk in get_lnk(data):
                soft.bin.append(lnk)
        if data.get('architecture'):
            bin_common = []
            if isinstance(soft.bin, list):
                bin_common = soft.bin
                soft.bin = {}
            for arch in ['64bit', '32bit']:
                if data.get('architecture').get(arch):
                    data_ = data['architecture'][arch]
                    if not data.get('url'):
                        url = data_['url']
                        soft.arch[arch] = url if scoop_rename else rename(url)
                        if soft.bin.get('hash'):
                            soft.sha256[arch] = data_['hash']
                    if get_bin(data_):
                        soft.bin[arch] = get_bin(data_) + bin_common
                    elif bin_common:
                        soft.bin[arch] = bin_common
                    if get_lnk(data_) and not soft.bin.get(arch):
                        soft.bin[arch] = []
                    for lnk in get_lnk(data_):
                        soft.bin[arch].append(lnk)

        if detail and data.get('homepage'):
            soft.homepage = data['homepage']
        if detail and data.get('description'):
            soft.description = data['description']
        return soft
