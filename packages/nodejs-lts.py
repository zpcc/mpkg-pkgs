import time

from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'nodejs-lts'

    def _prepare(self):
        data = self.data
        arch = {'32bit': 'https://nodejs.org/dist/v{ver}/node-v{ver}-x86.msi',
                '64bit': 'https://nodejs.org/dist/v{ver}/node-v{ver}-x64.msi'}
        url = 'https://nodejs.org/en/download/'
        data.ver = Search(url, 'LTS Version: <strong>([\\d.]+)</strong>')
        data.changelog = 'https://github.com/nodejs/node/tree/master/doc/changelogs'
        date = Search(
            f'https://nodejs.org/dist/v{data.ver}/', f'node-v{data.ver}-x64.msi</a>\\s+([\\w-]+)')
        data.date = time.strftime('%Y-%m-%d', time.strptime(date, '%d-%b-%Y'))
        data.arch = Search(links=arch, ver=data.ver)
        data.sha256 = Search(
            data.arch, sumurl=f'https://nodejs.org/dist/v{data.ver}/SHASUMS256.txt')
