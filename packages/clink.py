from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'clink'

    def _prepare(self):
        data = self.data
        data.bin = ['clink.bat']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/chrisant996/clink/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1][1:]
        for link in links:
            if link.endswith('.zip') and '_symbols.zip' not in link and '/archive/' not in link:
                data.links = [link]
