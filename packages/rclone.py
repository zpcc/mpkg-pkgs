from mpkg.common import Soft, get_bits, soft_data
from mpkg.load import Load
from mpkg.utils import SearchSum


class Package(Soft):
    ID = 'rclone'

    def _prepare(self):
        data = self.data
        data.bin = ['rclone.exe']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/rclone/rclone/releases/latest'
        header, links, data.date = parser(url)
        sumurl = [link for link in links if link.endswith('/SHA256SUMS')][0]
        data.changelog = url
        data.ver = header.split(' ')[-1]
        if data.ver.startswith('v'):
            data.ver = data.ver[1:]
        for link in links:
            if '-windows-amd64.zip' in link:
                data.arch['64bit'] = link
                data.sha256['64bit'] = SearchSum(link, sumurl)
            elif '-windows-386.zip' in link:
                data.arch['32bit'] = link
                data.sha256['32bit'] = SearchSum(link, sumurl)
        larch = {'32bit': f'https://github.com/rclone/rclone/releases/download/v{data.ver}/rclone-v{data.ver}-linux-386.deb',
                 '64bit': f'https://github.com/rclone/rclone/releases/download/v{data.ver}/rclone-v{data.ver}-linux-amd64.deb'}
        ldata = data.create_new(arch=larch)
        for bits, link in larch.items():
            assert link in links
            ldata.sha256[bits] = SearchSum(link, sumurl)
        ldata.bin = ['MPKG-DEB']
        self.append_arch(['linux', 'deb'], ldata)
        adata = soft_data()
        for arch in ['arm-v7', 'arm64']:
            bits = get_bits(arch)
            link = f'https://github.com/rclone/rclone/releases/download/v{data.ver}/rclone-v{data.ver}-linux-{arch}.deb'
            assert link in links
            adata.arch[bits] = link
            adata.sha256[bits] = SearchSum(link, sumurl)
        adata = adata.copyfrom(ldata)
        self.append_arch(['linux', 'arm', 'deb'], adata)
