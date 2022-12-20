import json
import os
import re

from lxml import etree
from mpkg.common import Soft, soft_data
from mpkg.config import GetConfig
from mpkg.utils import GetPage, MGet, logger


def get_gh_token():
    token = os.environ.get('GH_API_TOKEN')
    if not token:
        token = GetConfig('GH_API_TOKEN')
    if token:
        logger.debug('found gh token')
    return token


class Package(Soft):
    @staticmethod
    def sourceforge(url: str):
        if url.endswith('/download'):
            # input: https://sourceforge.net/projects/sevenzip/files/7-Zip/19.00/7z1900.exe/download
            # output: https://newcontinuum.dl.sourceforge.net/project/sevenzip/7-Zip/19.00/7z1900.exe
            # see also: https://sourceforge.net/projects/mpv-player-windows/rss?path=/stable
            project = re.findall(
                'https?://sourceforge.net/projects/(.*)', url)[0]
            result = 'https://downloads.sourceforge.net/project/' + \
                project[:-9].replace('/files/', '/')
            return result
        else:
            # input: https://sourceforge.net/projects/sevenzip/files/7-Zip/
            # output: [('19.00', '2019-02-22'), ('18.06', '2018-12-30')]
            #items = re.findall('net\.sf\.files = (.*);', GetPage(url))[0]
            folders = etree.HTML(GetPage(url)).xpath('//*[@class="folder "]')
            files = etree.HTML(GetPage(url)).xpath('//*[@class="file "]')
            result = [(item.xpath('.//span')[0].text,
                       item.xpath('.//abbr')[0].values()[0][:10]) for item in (folders+files)]
            return result

    @staticmethod
    def github(url: str, getall=False, regex='.*', raw=False):
        token = get_gh_token()
        headers = {"Authorization": f'Bearer {token}'} if token else {}
        if getall:
            rels = [rel for rel in json.loads(MGet(
                f'https://api.github.com/repos/{url}/releases', headers=headers).text) if re.match(regex, rel['name'])]
            if raw:
                return rels
            return [(rel['name'], [asset['browser_download_url'] for asset in rel['assets']],
                     rel['published_at'][:10]) for rel in rels]
        # input: https://github.com/git-for-windows/git/releases/latest
        # output: ('Git for Windows 2.27.0', ['https://github.com/git-for-wind...], '2020-06-01')
        owner, repo, tag = re.match(
            r'https?:\/\/github.com\/(.*)\/(.*)\/releases\/(.*)', url).groups()
        if tag.startswith('tag/'):
            tag = tag.replace('tag/', 'tags/')
        api_url = f'https://api.github.com/repos/{owner}/{repo}/releases/{tag}'
        rel = MGet(api_url, headers=headers).json()
        title = rel['name'] if rel['name'] else rel['tag_name']
        date = rel['published_at'][:10]
        assets = rel['assets']
        links = [x['browser_download_url'] for x in assets]
        if not links or not title:
            raise Exception('gh parser error')
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
