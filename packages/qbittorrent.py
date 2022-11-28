from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import Search


class Package(Soft):
    ID = 'qbittorrent'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].sourceforge
        url = 'https://sourceforge.net/projects/qbittorrent/files/qbittorrent-win32/'
        data.changelog = 'https://www.qbittorrent.org/news.php'
        ver, data.date = parser(url)[0]
        data.ver = ver.split('qbittorrent-')[1]
        links = [parser(url+ver+'/'+item[0]+'/download')
                 for item in parser(url+ver)]
        data.arch['64bit'] = [
            link for link in links if link.endswith('_x64_setup.exe')][0]
