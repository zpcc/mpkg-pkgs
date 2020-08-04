from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import Search


class Package(Soft):
    ID = 'qbittorrent'
    SilentArgs = '/S'

    def _prepare(self):
        parser = Load('http/common-zpcc.py', sync=False)[0][0].sourceforge
        url = 'https://sourceforge.net/projects/qbittorrent/files/qbittorrent-win32/'
        self.log = 'https://www.qbittorrent.org/news.php'
        ver, self.date = parser(url)[0]
        self.ver = ver.split('qbittorrent-')[1]
        links = [parser(url+ver+'/'+item[0]+'/download')
                 for item in parser(url+ver)]
        for link in links:
            if link.endswith('.exe'):
                if link.endswith('_x64_setup.exe'):
                    self.link['64bit'] = link
                else:
                    self.link['32bit'] = link
