from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'veracrypt'

    def _prepare(self):
        data = self.data
        parser = Load('http/common-zpcc.py', sync=False)[0][0].launchpad
        url = 'https://launchpad.net/veracrypt/trunk'
        data.changelog = 'https://ultradefrag.net/HISTORY.TXT'
        ver, url, data.date = parser(url)[0]
        data.ver = ver.split(' ')[1]
        links = parser(url)
        link = [link for link in links if link.endswith(
            '.exe') and 'Setup' in link][0].replace('%20', ' ')
        data.changelog = [u for u in links if u.endswith('README.TXT')][0]
        txt = GetPage([u for u in links if u.endswith('sha256sum.txt')][0])
        sha256 = [line for line in txt.splitlines() if line.endswith(
            link.split('/')[-1])][0].split(' ')[0]
        data.links = [link]
        data.sha256 = {'32bit': sha256, '64bit': sha256}
