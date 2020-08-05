import time

from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'adb'
    BIN = ['adb.exe', 'fastboot.exe']

    def _prepare(self):
        link = [
            'https://dl.google.com/android/repository/platform-tools_r{ver}-windows.zip']
        url = 'https://developer.android.com/studio/releases/platform-tools?hl=en'
        self.log = url
        self.ver = Search(url, '<h4.*>([\\d.]+) \\(.*\\)</h4>')
        self.links = Search(links=link, ver=self.ver)
        date = Search(url, '<h4.*>[\\d.]+ \\((.*)\\)</h4>')
        self.date = time.strftime('%Y-%m-%d', time.strptime(date, '%B %Y'))
