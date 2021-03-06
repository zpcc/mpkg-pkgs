from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'googlechrome'

    def _prepare(self):
        parser = Load('http/common-zpcc.py', sync=False)[0][0].scoop
        url = 'https://github.com/lukesampson/scoop-extras/raw/master/bucket/googlechrome.json'
        self.data = parser(url)
