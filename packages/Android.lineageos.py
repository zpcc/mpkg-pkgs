from mpkg.common import Soft
from mpkg.utils import GetPage, Search


class Package(Soft):
    ID = 'lineageos.download'
    needConfig = True

    def __init__(self):
        super().__init__()
        self.dname = self.getconfig('device name')

    def config(self):
        super().config()
        self.setconfig('device name')

    def _prepare(self):
        if not self.dname:
            return
        url = f'https://lineageos.mirrorhub.io/full/{self.dname}/'
        ver = Search(url, r'([\d]{8})/</a>', reverse=True)
        links = Search(f'{url}{ver}/', r'href="(.*)"', findall=True)
        links.remove('../')
        self.data.ver = ver
        self.data.links = [f'{url}{ver}/{link}' for link in links]
