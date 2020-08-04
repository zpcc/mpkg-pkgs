from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'mpv.portable'
    BIN = ['mpv.com']

    def _prepare(self):
        parser = Load('http/common-zpcc.py', sync=False)[0][0].sourceforge
        url = 'https://sourceforge.net/projects/mpv-player-windows/files/stable/'
        self.log = 'https://github.com/mpv-player/mpv/releases'
        items = parser(url)
        file, self.date = [(file, date)
                           for file, date in items[:2] if 'x86_64' in file][0]
        self.ver = file.split('-')[1]
        file32 = [file for file, date in items[:2] if 'i686' in file][0]
        self.link = {'64bit': parser(url+file+'/download'),
                     '32bit': parser(url+file32+'/download')}
