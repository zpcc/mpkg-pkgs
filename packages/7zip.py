from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import Search


class Package(Soft):
    ID = '7zip'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].sourceforge
        data.changelog = 'https://www.7-zip.org/history.txt'
        data.ver = Search('https://www.7-zip.org/download.html',
                          'Download 7-Zip ([\\d.]+)')
        url = 'https://sourceforge.net/projects/sevenzip/files/7-Zip/'+data.ver
        L = parser(url)
        data.date = L[0][1]
        links = [parser(url+'/'+item[0]+'/download') for item in L]
        for link in links:
            if link.endswith('.exe'):
                if link.endswith('-x64.exe'):
                    data.arch['64bit'] = link
                else:
                    data.arch['32bit'] = link
