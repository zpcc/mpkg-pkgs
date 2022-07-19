from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import SearchSum


class Package(Soft):
    ID = 'rclone'

    def _prepare(self):
        data = self.data
        data.bin = ['rclone.exe']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/rclone/rclone/releases/latest'
        header, links, data.date = parser(url)
        sumurl = [link for link in links if link.endswith('/SHA256SUMS')][0]
        data.changelog = url
        data.ver = header.split(' ')[-1]
        if data.ver.startswith('v'):
            data.ver = data.ver[1:]
        for link in links:
            if '-windows-amd64.zip' in link:
                data.arch['64bit'] = link
                data.sha256['64bit'] = SearchSum(link, sumurl)
            elif '-windows-386.zip' in link:
                data.arch['32bit'] = link
                data.sha256['32bit'] = SearchSum(link, sumurl)
