from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import SearchSum


class Package(Soft):
    ID = 'nali'

    def _prepare(self):
        data = self.data
        data.bin = {'32bit': [['nali-windows-386.exe', 'nali']],
                    '64bit': [['nali-windows-amd64.exe', 'nali']]}
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/zu1k/nali/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1]
        if data.ver.startswith('v'):
            data.ver = data.ver[1:]
        for link in links:
            if '-windows-amd64-' in link and link.endswith('.zip'):
                data.arch['64bit'] = link
                data.sha256['64bit'] = SearchSum(link, link+'.sha256')
            elif '-windows-386-' in link and link.endswith('.zip'):
                data.arch['32bit'] = link
                data.sha256['32bit'] = SearchSum(link, link+'.sha256')
