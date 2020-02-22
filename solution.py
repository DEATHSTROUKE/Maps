import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5 import uic, Qt
from PyQt5 import QtCore


class Maps(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('des.ui', self)
        self.x = '55.753215'
        self.y = '37.622504'
        self.z = '5'
        self.l = 'map'
        self.photo = 'map.png'
        self.schema.clicked.connect(lambda: self.change_type_map('map'))
        self.sput.clicked.connect(lambda: self.change_type_map('sat'))
        self.gibrid.clicked.connect(lambda: self.change_type_map('sat,skl'))
        self.getImage()

    def change_type_map(self, type1):
        self.l = type1
        if self.l != 'map':
            self.photo = 'map.jpg'
        else:
            self.photo = 'map.png'
        self.getImage()

    def keyPressEvent(self, event):
        try:
            if event.key() == QtCore.Qt.Key_PageUp:
                if int(self.z) < 18:
                    self.z = str(int(self.z) + 1)
                    self.getImage()
            if event.key() == QtCore.Qt.Key_PageDown:
                if 0 <= int(self.z):
                    self.z = str(int(self.z) - 1)
                    self.getImage()
        except BaseException:
            pass
        if event.key() == QtCore.Qt.Key_Up:
            self.shift = 450 * 180 / 2 ** (int(self.z) + 8)
            if float(self.x) + self.shift < 90:
                self.x = str(float(self.x) + self.shift)
                self.getImage()
                print(self.x, self.y)

        if event.key() == QtCore.Qt.Key_Down:
            self.shift = 450 * 180 / 2 ** (int(self.z) + 8)
            if float(self.x) - self.shift > -90:
                self.x = str(float(self.x) - self.shift)
                self.getImage()
                print(self.x, self.y)

        if event.key() == QtCore.Qt.Key_Left:
            self.shift = 600 * 360 / 2 ** (int(self.z) + 8)
            if float(self.y) - self.shift > -180:
                self.y = str(float(self.y) - self.shift)
                self.getImage()
                print(self.x, self.y)

        if event.key() == QtCore.Qt.Key_Right:
            self.shift = 600 * 360 / 2 ** (int(self.z) + 8)
            if float(self.y) + self.shift < 180:
                self.y = str(float(self.y) + self.shift)
                self.getImage()
                print(self.x, self.y)

    def getImage(self):
        url = "http://static-maps.yandex.ru/1.x/"
        params = {'ll': f'{self.y},{self.x}', 'z': f'{self.z}', 'l': self.l, 'size': '600,450'}
        response = requests.get(url, params=params)

        if not response:
            print("Ошибка выполнения запроса")
            print("Http статус:", response.status_code, "(", response.reason, ")")
        else:
            self.map_file = self.photo
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            self.setImage()

    def setImage(self):
        self.pix = QPixmap(self.map_file)
        # self.pix = self.pix.scaledToWidth(512)
        # self.pix = self.pix.scaledToHeight(512)
        self.lbl.setPixmap(self.pix)

    def closeEvent(self, event):
        try:
            os.remove(self.map_file)
        except BaseException:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    n = Maps()
    n.show()
    sys.exit(app.exec())
