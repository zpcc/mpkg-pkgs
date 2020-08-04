from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'TrafficMonitor.install'
    BIN = ['PORTABLE']
    CMD = {'start': 'taskkill /im TrafficMonitor.exe /t >nul',
           'end': 'cd /d "{root}" && start TrafficMonitor.exe'}

    def _prepare(self):
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/zhongyang219/TrafficMonitor/releases/latest'
        header, links, self.date = parser(url)
        self.log = url
        self.ver = header.split('V')[1]
        for link in links:
            if link.endswith('_x64.7z'):
                self.link['64bit'] = link
            elif link.endswith('_x86.7z'):
                self.link['32bit'] = link
