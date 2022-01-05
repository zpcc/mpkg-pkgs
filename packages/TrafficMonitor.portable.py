from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'TrafficMonitor.portable'

    def _prepare(self):
        data = self.data
        data.bin = ['MPKG-PORTABLE']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/zhongyang219/TrafficMonitor/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split('V')[1]
        for link in links:
            if link.endswith('_x64.7z') or link.endswith('_x64.zip'):
                data.arch['64bit'] = link
            elif link.endswith('_x86.7z') or link.endswith('_x86.zip'):
                data.arch['32bit'] = link
