from mpkg.common import Soft
from mpkg.load import Load
from mpkg.utils import Search


class Package(Soft):
    ID = 'sqlitebrowser'

    def _prepare(self):
        data = self.data
        data.args = '/qn /norestart'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        tag = parser('sqlitebrowser/sqlitebrowser', getall=True,
                     regex=r'^DB Browser for SQLite [\d.]*$', raw=True)[0]['tag_name']
        url = 'https://github.com/sqlitebrowser/sqlitebrowser/releases/' + tag
        header, links, data.date = parser(url)
        data.changelog = url
        data.ver = header.split(' ')[-1]
        for link in links:
            if link.endswith('-win64.msi'):
                data.arch['64bit'] = link
            elif link.endswith('-win32.msi'):
                data.arch['32bit'] = link
        for k, v in data.arch.items():
            sha256 = Search(url, v.split('/')[-1] +
                            '\\s*<ul>\\s*<li>(\\S*)</li>')
            if sha256:
                data.sha256[k] = sha256
