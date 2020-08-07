from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = '7zip'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].sourceforge
        url = 'https://sourceforge.net/projects/sevenzip/files/7-Zip/'
        data.changelog = 'https://www.7-zip.org/history.txt'
        ver, data.date = parser(url)[0]
        data.ver = ver
        links = [parser(url+ver+'/'+item[0]+'/download')
                 for item in parser(url+ver)]
        for link in links:
            if link.endswith('.exe'):
                if link.endswith('-x64.exe'):
                    data.arch['64bit'] = link
                else:
                    data.arch['32bit'] = link
