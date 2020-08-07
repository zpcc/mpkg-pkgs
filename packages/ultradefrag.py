from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'ultradefrag'

    def _prepare(self):
        data = self.data
        data.args = '/S /FULL=1'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].sourceforge
        url = 'https://sourceforge.net/projects/ultradefrag/files/stable-release/'
        data.changelog = 'https://ultradefrag.net/HISTORY.TXT'
        data.ver, data.date = parser(url)[0]
        links = [parser(url+data.ver+'/'+item[0]+'/download')
                 for item in parser(url+data.ver)]
        for link in links:
            if link.endswith('.amd64.exe'):
                data.arch['64bit'] = link
            elif link.endswith('.i386.exe'):
                data.arch['32bit'] = link
