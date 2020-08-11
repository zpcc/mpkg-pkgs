from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'nomacs'

    def _prepare(self):
        data = self.data
        data.args = '/quiet /norestart'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/nomacs/nomacs/releases/latest'
        data.ver, links, data.date = parser(url)
        data.changelog = url
        for link in links:
            if link.endswith('-setup-x64.msi'):
                data.arch['64bit'] = link
