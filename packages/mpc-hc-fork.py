from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'mpc-hc-fork'

    def _prepare(self):
        data = self.data
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        rel = [rel for rel in parser(
            'clsid2/mpc-hc', getall=True) if rel[0] != 'Development build'][0]
        header, links, data.date = rel
        data.changelog = 'https://github.com/clsid2/mpc-hc/releases'
        data.ver = header.split(' ')[-1]
        for link in links:
            if link.endswith('.x64.exe'):
                data.arch['64bit'] = link
            elif link.endswith('.x86.exe'):
                data.arch['32bit'] = link
