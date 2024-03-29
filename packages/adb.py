import time

from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'adb'

    def _prepare(self):
        data = self.data
        data.bin = ['adb.exe', 'fastboot.exe']
        data.cmd = {'start': 'adb kill-server 2>nul'}
        links = [
            'https://dl.google.com/android/repository/platform-tools_r{ver}-windows.zip']
        url = 'https://developer.android.com/studio/releases/platform-tools?hl=en'
        data.changelog = url
        data.ver = Search(url, '<h4.*>([\\d.]+) \\(.*\\)</h4>')
        data.links = Search(links=links, ver=data.ver)
        date = Search(url, '<h4.*>[\\d.]+ \\((.*)\\)</h4>')
        try:
            data.date = time.strftime('%Y-%m-%d', time.strptime(date, '%B %Y'))
        except ValueError:
            try:
                data.date = time.strftime('%Y-%m-%d', time.strptime(date, '%b %Y'))
            except Exception:
                print('failed to parse date')
