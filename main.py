from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout, 
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 
from PIL import Image, ImageFilter
import os

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle("Easy Editor")

lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
btn_dir.setStyleSheet('background-color: yellow; color: black;')
lw_files = QListWidget()

#робимо кнопки і міняємо коліркнопок
btn_left = QPushButton('Лево')
btn_left.setStyleSheet('background-color: yellow; color: black;')
btn_right = QPushButton('Право')
btn_right.setStyleSheet('background-color: yellow; color: black;')
btn_flip = QPushButton('Зеркало')
btn_flip.setStyleSheet('background-color: yellow; color: black;')
btn_sharp = QPushButton('Резкость')
btn_sharp.setStyleSheet('background-color: yellow; color: black;')
btn_bw = QPushButton('Ч/Б')
btn_bw.setStyleSheet('background-color: yellow; color: black;')



col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)

col2.addWidget(lb_image)

#мистворюємо лінію 
row = QHBoxLayout()
row.addWidget(btn_left)
row.addWidget(btn_right)
row.addWidget(btn_flip)
row.addWidget(btn_sharp)
row.addWidget(btn_bw)

col2.addLayout(row)

layout_main = QHBoxLayout()
layout_main.addLayout(col1)
layout_main.addLayout(col2)

win.setLayout(layout_main)

# filtrue foto vid texta
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result



#вибираэ фото 
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

#вказує імена фото
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
 
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)



btn_dir.clicked.connect(showFilenamesList)

#процес обробки фото
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "edited/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self,path):
        lb_image.hide()
        piximage = QPixmap(path)
        w = lb_image.width()
        h = lb_image.height()
        piximage = piximage.scaled(w, h, Qt.KeepAspectRatio)

        lb_image.setPixmap(piximage)
        lb_image.show()


    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if os.path.exists(path) or os.path.isdir(path):
            image_path = os.path.join(path, self.filename)
            self.image.save(image_path)

        else:
            os.mkdir(path)

         #чорно быле
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)



    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self): #зеркало
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharp(self): #розмиття
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)




workimage = ImageProcessor()
#показує фотояке ми вибрали
def showChosenImage():
   if lw_files.currentRow() >= 0:
       filename = lw_files.currentItem().text()
       workimage.loadImage(workdir, filename)
       image_path = os.path.join(workimage.dir, workimage.filename)
       workimage.showImage(image_path)
 


lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharp)

win.show()
app.exec()
