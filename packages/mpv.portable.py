from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'mpv.portable'

    def _prepare(self):
        data = self.data
        data.bin = ['mpv.com']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].sourceforge
        url = 'https://sourceforge.net/projects/mpv-player-windows/files/release/'
        data.changelog = 'https://github.com/mpv-player/mpv/releases'
        items = parser(url)
        items = [x for x in items if 'mpv-dev-' not in x[0]]
        file, data.date = [(file, date)
                           for file, date in items[:3] if 'x86_64.7z' in file][0]
        data.ver = file.split('-')[1]
        file32 = [file for file, date in items[:3] if 'i686.7z' in file][0]
        data.arch = {'64bit': parser(url+file+'/download'),
                     '32bit': parser(url+file32+'/download')}
