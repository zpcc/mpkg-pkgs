from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = '7zip'
    SilentArgs = '/S'

    def _prepare(self):
        parser = Load(
            'https://github.com/zpcc/mpkg-pkgs/raw/master/parser/common.py')[0][0].sourceforge
        url = 'https://sourceforge.net/projects/sevenzip/files/7-Zip/'
        ver, self.date = parser(url)[0]
        self.ver = ver
        links = [parser(url+ver+'/'+item[0]+'/download')
                 for item in parser(url+ver)]
        self.link = {}
        for link in links:
            if link.endswith('.exe'):
                if link.endswith('-x64.exe'):
                    self.link['64bit'] = link
                else:
                    self.link['32bit'] = link
