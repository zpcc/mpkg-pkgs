from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import GetPage


class Package(Soft):
    ID = 'vcredist-all-x64'

    def _prepare(self):
        data = self.data
        data.depends = []
        data.ver = 'vc2013'
        args = '/quiet /norestart'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].scoop

        files = ['vcredist2005', 'vcredist2008',
                 'vcredist2010', 'vcredist2012', 'vcredist2013']
        urls = [
            f'gh/ScoopInstaller/Extras@master/bucket/{u}.json' for u in files]
        url = 'https://cdn.jsdelivr.net/combine/'+','.join(urls)
        page = GetPage(url)

        def sortlinks(data):
            for link in data.links:
                name = link.split('/')[-1].lower()
                if 'x64.exe' in name:
                    data.sha256 = [data.sha256[data.links.index(link)]]
                    data.links = [link]
                    break

        for i, item in enumerate(page.split('\n\n\n')):
            soft = parser(data=item, detail=False)
            soft.id = files[i]+'-x64'
            sortlinks(soft)
            soft.args = args
            data.depends.append(soft.id)
            self.packages.append(soft.asdict(simplify=True))
