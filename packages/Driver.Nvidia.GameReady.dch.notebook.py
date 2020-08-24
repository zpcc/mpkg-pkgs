from mpkg.common import Soft
from mpkg.load import Load


class Package(Soft):
    ID = 'GeForceGameReadyDriver.dch.notebook'
    allowExtract = True

    def _prepare(self):
        data = self.data
        pkg = Load(
            'https://github.com/zpcc/mpkg-pkgs/raw/master/packages/Driver.Nvidia.py->parser-NvidiaGameReadyDriver.dch.notebook.py')[0][0]
        pkg.url = 'https://www.nvidia.com/Download/processFind.aspx?psid=111&pfid=919&osid=57&lid=1&dtcid=1'
        pkg.isStudio = False
        pkg.prepare()
        data_ = pkg.data
        data.ver, data.date, data.arch, data.changelog = data_.ver, data_.date, data_.arch, data_.changelog
