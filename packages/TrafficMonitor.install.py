from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'TrafficMonitor.install'

    def _prepare(self):
        data = self.data
        data.bin = ['MPKG-PORTABLE']
        data.cmd = {'start': 'taskkill /im TrafficMonitor.exe /t >nul',
                    'end': 'cd /d "{root}" && start TrafficMonitor.exe'}
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/zhongyang219/TrafficMonitor/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split('V')[1]
        for link in links:
            if '_x64_without_temperature' in link:
                data.arch['64bit'] = link
            elif '_x86_without_temperature' in link:
                data.arch['32bit'] = link
