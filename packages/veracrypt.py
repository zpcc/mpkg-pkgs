from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import SearchSum


class Package(Soft):
    ID = 'veracrypt'

    def _prepare(self):
        data = self.data
        parser = Load('http/common-zpcc.py', sync=False)[0][0].launchpad
        url = 'https://launchpad.net/veracrypt/trunk'
        data.changelog = 'https://ultradefrag.net/HISTORY.TXT'
        L = parser(url)
        ver, url, data.date = L[0]
        data.ver = ver.split(' ')[1]
        links = parser(url)
        # https://launchpad.net/veracrypt/trunk/1.25.4/+download/VeraCrypt_Setup_x64_1.25.4.msi
        # https://www.veracrypt.fr/en/Downloads.html
        link = [link for link in links if link.endswith(
            '.exe') and 'Setup' in link and 'TESTSIGNING' not in link][0].replace('%20', ' ')
        data.changelog = [u for u in links if u.endswith('README.TXT')][0]
        data.links = [link]
        sumurl = [u for u in links if u.endswith('sha256sum.txt')]
        if sumurl:
            data.sha256 = SearchSum(data.links, sumurl[0])
        else:
            data.sha256 = []
            for url in data.links:
                data.sha256.append('md5:'+SearchSum(url, link+'/+md5'))
