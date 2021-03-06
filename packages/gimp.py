from lxml import etree
from mpkg.common import Soft
from mpkg.utils import GetPage, Search


class Package(Soft):
    ID = 'gimp'

    def _prepare(self):
        data = self.data
        data.args = '/VERYSILENT /NORESTART /SUPPRESSMSGBOXES /SP-'
        data.changelog = 'https://www.gimp.org/release-notes/'
        url = 'https://www.gimp.org/'
        v = etree.HTML(GetPage(url)).xpath('//*[@id="ver"]')[0].text
        v_ = '.'.join(v.split('.')[:2])
        url2 = f'https://download.gimp.org/mirror/pub/gimp/v{v_}/windows/'
        v2 = Search(url2, f'gimp-{v}-setup-([\\d]+).exe', findall=True)
        if v2:
            v2 = v2[-1]
            data.ver = f'{v}_{v2}'
            filename = f'gimp-{v}-setup-{v2}.exe'
        else:
            data.ver = v
            filename = f'gimp-{v}-setup.exe'
        data.links = [url2 + filename]
        data.sha256 = Search(data.links, sumurl=url2+'SHA256SUMS')
