import re
import time

from lxml import etree
from mpkg.common import Soft, soft_data
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'python-stable'

    def _prepare(self):
        data = self.data
        url = 'https://www.python.org/ftp/python/'
        texts = list(etree.HTML(GetPage(url)).xpath('//pre')[0].itertext())[2:]
        rels = [name[:-1] for name in texts[::2]
                if re.match('^\\d.[\\d.]+/', name)]
        page = etree.HTML(GetPage('https://devguide.python.org/'))
        table = page.xpath('//*[@id="status-of-python-branches"]//table')[0]
        table = [[text.strip() for text in tr]
                 for tr in [list(tr.itertext()) for tr in table.xpath('.//tr')]]
        active = [tr[0] for tr in table if 'bugfix' in tr]
        data.ver = sorted(active, key=lambda x: int(x.split('.')[1]))[-1]
        for ver in active:
            soft = soft_data()
            soft.id = f'python{ver}'
            data.depends.append(soft.id)
            rel = sorted([rel for rel in rels if rel.startswith(ver)],
                         key=lambda x: int(x.split('.')[2]))[-1]
            soft.ver = rel
            date = texts[texts.index(rel+'/')+1].strip().split(' ')[0]
            soft.date = time.strftime(
                '%Y-%m-%d', time.strptime(date, '%d-%b-%Y'))
            soft.arch = {'32bit': f'https://www.python.org/ftp/python/{soft.ver}/python-{soft.ver}.exe',
                         '64bit': f'https://www.python.org/ftp/python/{soft.ver}/python-{soft.ver}-amd64.exe'}
            soft.changelog = f'https://docs.python.org/release/{soft.ver}/whatsnew/changelog.html#changelog'
            relpage = etree.HTML(GetPage(
                'https://www.python.org/downloads/release/python-{0}/'.format(soft.ver.replace('.', ''))))
            files = relpage.xpath('//tbody/tr')
            md5 = {}
            for tr in files:
                td = tr.xpath('./td')
                url = td[0].xpath('./a')[0].values()[0]
                md5[url] = td[3].text
            soft.sha256 = {'32bit': 'md5:' + md5[soft.arch['32bit']],
                           '64bit': 'md5:' + md5[soft.arch['64bit']]}
            self.packages.append(soft.asdict(simplify=True))
