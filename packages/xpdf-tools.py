import time

from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'xpdf-tools'

    def _prepare(self):
        data = self.data
        Bin = ["pdftopng.exe", "pdftoppm.exe", "pdfimages.exe", "pdftohtml.exe",
               "pdffonts.exe", "pdfdetach.exe", "pdftotext.exe", "pdfinfo.exe", "pdftops.exe"]
        data.bin = {'32bit': ['bin32\\'+file for file in Bin],
                    '64bit': ['bin64\\'+file for file in Bin]}
        #links = ['https://dl.xpdfreader.com/xpdf-tools-win-{ver}.zip']
        links = [
            'https://xpdfreader-dl.s3.amazonaws.com/xpdf-tools-win-{ver}.zip']
        url = 'https://www.xpdfreader.com/download.html'
        data.ver = Search(url, 'Current version:\\s*([^\\s<]+)')
        data.links = Search(links=links, ver=data.ver)
        date = Search(url, 'Released:\\s*([\\S ]*)<')
        data.date = time.strftime('%Y-%m-%d', time.strptime(date, '%Y %b %d'))
