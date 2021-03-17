from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'shimexe_kiennq'

    def _prepare(self):
        data = self.data
        data.bin = ['MPKG-PORTABLE']
        #loc = Path(GetConfig('files_dir')) / 'shimexe_kiennq' / 'shim.exe'
        #data.notes = 'please set up shimexe manually'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/kiennq/scoop-better-shimexe/releases/latest'
        data.ver, links, data.date = parser(url)
        data.changelog = url
        data.links = [link for link in links if '/shimexe-' in link]
