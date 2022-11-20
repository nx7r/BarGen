import math

from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image


class BarGen():
    def __init__(self,codes = []) -> None:
        self.codes = codes
        self.barcodes = []
        self.pages = []
    
    def clear(self):
        self.codes = []
        self.barcodes = []
        self.pages = []

    def clear_pages(self):
        self.pages = []

    def generate(self,start, end, ret = False):
        for i in range(abs(end-start)+1):
            self.codes.append(str(start+i))
        if ret:
            return self.codes

    def render(self, ret = False):
        for code in self.codes:
            bc = Code128(str(code), writer=ImageWriter()).render()
            bc.resize((512,280))
            self.barcodes.append(bc)
        if ret:
            return self.barcodes
    
    def render_pages(self, raws, colums, auto_render= False, ret = False):
        if auto_render:
            self.render()
        max_in_page = raws*colums
        pages_count = math.ceil(len(self.barcodes) /max_in_page)
        i = 0
        for page in range(pages_count):
            dst = Image.new('RGB', (self.barcodes[0].width*colums, self.barcodes[0].height*raws))
            for r in range(raws):
                for c in range(colums):
                    if i+1 > len(self.barcodes):
                        break
                    dst.paste(self.barcodes[i], (c*self.barcodes[i].width, r*self.barcodes[i].height))
                    i += 1
            self.pages.append(dst)
        
        if ret:
            return self.pages