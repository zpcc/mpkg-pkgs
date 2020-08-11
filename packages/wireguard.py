import json

from mpkg.common import Soft
from mpkg.utils import GetPage, Search


class Package(Soft):
    ID = 'wireguard'

    def _prepare(self):
        data = self.data
        data.args = '/qn /norestart'
        links = {'32bit': 'https://download.wireguard.com/windows-client/wireguard-x86-{ver}.msi',
                 '64bit': 'https://download.wireguard.com/windows-client/wireguard-amd64-{ver}.msi'}
        url = 'https://build.wireguard.com/distros.json'
        data.ver = json.loads(GetPage(url))['windowsdl-win']['version']
        data.changelog = f'https://www.wireshark.org/docs/relnotes/wireshark-{data.ver}.html'
        data.arch = Search(links=links, ver=data.ver)
