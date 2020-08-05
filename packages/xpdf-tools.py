import time

from mpkg.common import Soft
from mpkg.utils import Search


class Package(Soft):
    ID = 'xpdf-tools'
    Bin = ["pdftopng.exe", "pdftoppm.exe", "pdfimages.exe", "pdftohtml.exe",
           "pdffonts.exe", "pdfdetach.exe", "pdftotext.exe", "pdfinfo.exe", "pdftops.exe"]
    BIN = {'32bit': ['bin32\\'+file for file in Bin],
           '64bit': ['bin64\\'+file for file in Bin]}

    def _prepare(self):
        #link = ['https://dl.xpdfreader.com/xpdf-tools-win-{ver}.zip']
        link = [
            'https://xpdfreader-dl.s3.amazonaws.com/xpdf-tools-win-{ver}.zip']
        url = 'https://www.xpdfreader.com/download.html'
        self.ver = Search(url, 'Current version:\\s*([^\\s<]+)')
        self.links = Search(links=link, ver=self.ver)
        date = Search(url, 'Released:\\s*([\\S ]*)<')
        self.date = time.strftime('%Y-%m-%d', time.strptime(date, '%Y %b %d'))
