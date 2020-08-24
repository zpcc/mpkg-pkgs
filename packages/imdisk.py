from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'imdisk'

    def _prepare(self):
        data = self.data
        data.bin = ['MPKG-PORTABLE']
        data.cmd = {
            'end': '"{root}\\install.bat"\necho please execute rmdir /s /q "{root}" after installtion'}
        parser = Load('http/common-zpcc.py', sync=False)[0][0].sourceforge
        url = 'https://sourceforge.net/projects/imdisk-toolkit/files/'
        data.changelog = url
        ver, data.date = parser(url)[0]
        data.ver = ver
        links = [parser(url+ver+'/'+item[0]+'/download')
                 for item in parser(url+ver)]
        for link in links:
            if link.endswith('.zip'):
                if link.endswith('-x64.zip'):
                    data.arch['64bit'] = link
                else:
                    data.arch['32bit'] = link
