from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'workrave'

    def _prepare(self):
        data = self.data
        data.args = '/verysilent /norestart'
        parser = Load('http/common-zpcc.py', sync=False)[0][0].github
        url = 'https://github.com/rcaelers/workrave/releases/latest'
        header, links, data.date = parser(url)
        data.changelog = 'https://workrave.org/blog/'
        data.ver = header.split(' ')[-1]
        data.links = [link for link in links if link.endswith(
            '.exe') and 'Debug' not in link]
