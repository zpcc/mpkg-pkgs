from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'geogebra6'

    def _prepare(self):
        data = self.data
        data.args = '/S'
        # https://download.geogebra.org/installers/version.txt
        url = 'https://download.geogebra.org/installers/6.0/'
        data.ver = Search(
            url, 'GeoGebra-Windows-Installer-6-0-([\\d-]+).exe', reverse=True)
        data.links = [
            f'https://download.geogebra.org/installers/6.0/GeoGebra-Windows-Installer-6-0-{data.ver}.exe']
