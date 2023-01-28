from mpkg.common import Soft, soft_data
from mpkg.load import Load


class Package(Soft):
    ID = 'alist'

    def _prepare(self):
        data = self.data
        data.bin = ['alist.exe']
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/alist-org/alist/releases/latest'
        v, links, data.date = parser(url)
        data.ver = v[1:] if v.startswith('v') else v
        ldata, adata = soft_data(), soft_data()
        ldata.bin = ['alist']
        for link in links:
            if 'windows-amd64' in link:
                data.arch['64bit'] = link
            elif 'windows-386' in link:
                data.arch['32bit'] = link
            elif 'linux-amd64.' in link:
                ldata.arch['64bit'] = link
            elif 'linux-386.' in link:
                ldata.arch['32bit'] = link
            elif 'linux-arm64.' in link:
                adata.arch['64bit'] = link
            elif 'linux-arm-7.' in link:
                adata.arch['32bit'] = link
        ldata = ldata.copyfrom(data)
        self.append_arch(['linux'], ldata)
        self.append_arch(['linux', 'arm'], adata.copyfrom(ldata))
