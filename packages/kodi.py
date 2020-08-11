from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'kodi'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        arch = {'32bit': 'https://mirrors.kodi.tv/releases/windows/win32/kodi-{ver}-x86.exe',
                '64bit': 'https://mirrors.kodi.tv/releases/windows/win64/kodi-{ver}-x64.exe'}
        url = 'https://mirrors.kodi.tv/releases/windows/win64/?C=N&O=A'
        ver_ = Search(url, 'kodi-([\\d.]+-\\S+?)-x64.exe', reverse=True)
        data.ver = ver_.split('-')[0]
        data.arch = Search(links=arch, ver=ver_)
        for a in arch.keys():
            data.sha256[a] = Search(
                data.arch[a], sumurl=data.arch[a]+'.sha256', redirect=False)
