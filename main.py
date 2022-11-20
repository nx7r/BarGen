from PySide6.QtWidgets import QApplication, QListWidgetItem, QFileDialog, QLCDNumber
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6 import QtCore

from PIL.ImageQt import ImageQt
from bar_gen import BarGen
import random



class App():
    def __init__(self) -> None:
        
        self.loader = QUiLoader()
        
        self.app = QApplication([])

        self.bargen = BarGen()
        self.viewimg = QPixmap()

        self.ui = self.loader.load('main.ui', None)
        self.ui.show()

        self.ui.gen.clicked.connect(self.generate)
        self.ui.expo.clicked.connect(self.export)
        self.ui.apply.clicked.connect(self.apply)
        self.ui.add.clicked.connect(self.add)

    def generate(self):
        self.bargen.clear()
        self.bargen.generate(int(self.ui.start.text()),int(self.ui.end.text()))
        self.ui.datalist.clear()
        for code in self.bargen.codes:
            self.ui.datalist.addItem(QListWidgetItem(code))
        self.apply()
    
    def render(self):
        r, c = abs(int(self.ui.raws.text())) , abs(int(self.ui.colums.text()))
        self.bargen.render_pages(r, c, True, ret=True)
        pass

    def export(self):
        r, c = abs(int(self.ui.raws.text())) , abs(int(self.ui.colums.text()))
        if r*c:
            return
        dir = QFileDialog.getExistingDirectory(self.ui, "save to")
        if dir:
            pages = self.bargen.render_pages(r, c, True, ret=True)
            i = 0
            for page in pages:
                name = dir+str(i)+'.png'
                print('Saving::',name)
                page.save(name)
                i += 1


    def add(self):
        if self.ui.add_line.text() != "":
            code = self.ui.add_line.text()
            self.bargen.codes.append(code)
            self.ui.datalist.addItem(QListWidgetItem(code))


    def apply(self):
        self.bargen.clear_pages()
        self.render()
        print(self.bargen.pages)
        if self.bargen.pages != []:
            self.viewimg = QPixmap(ImageQt(self.bargen.pages[0]))
            self.ui.img.setPixmap(self.viewimg)
        self.ui.pages.display(len(self.bargen.pages))




    def mainloop(self):
        self.app.exec()




app = App()

app.mainloop()








"""

gen = BarGen()
gen.generate(10, 20)
pages = gen.render_pages(7, 5, True, True)
for page in pages:
    name = str(random.randint(0,50000))+'.png'
    print(name)
    page.save(name)

"""