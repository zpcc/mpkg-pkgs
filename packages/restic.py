from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import SearchSum


class Package(Soft):
    ID = 'restic'

    def _prepare(self):
        data = self.data
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/restic/restic/releases/latest'
        header, links, data.date = parser(url)
        sumurl = [link for link in links if link.endswith('/SHA256SUMS')][0]
        data.changelog = url
        data.ver = header.split(' ')[-1]
        data.ver = data.ver[1:] if data.ver.startswith('v') else data.ver
        data.bin = {'32bit': [[f'restic_{data.ver}_windows_386.exe', 'restic']],
                    '64bit': [[f'restic_{data.ver}_windows_amd64.exe', 'restic']]}
        for link in links:
            if '_windows_amd64.zip' in link:
                data.arch['64bit'] = link
                data.sha256['64bit'] = SearchSum(link, sumurl)
            elif '_windows_386.zip' in link:
                data.arch['32bit'] = link
                data.sha256['32bit'] = SearchSum(link, sumurl)
