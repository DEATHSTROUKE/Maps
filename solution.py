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
        self.coords = '37.622504,55.753215'
        self.z = '5'
        self.getImage()

    def keyPressEvent(self, event):
        try:
            if event.key() == QtCore.Qt.Key_PageUp:
                if 0 <= int(self.z) < 18:
                    self.z = str(int(self.z) + 1)
                    print(self.z)
                    self.getImage()
            if event.key() == QtCore.Qt.Key_PageDown:
                if 0 <= int(self.z) < 18:
                    self.z = str(int(self.z) - 1)
                    print(self.z)
                    self.getImage()
        except BaseException:
            pass

    def getImage(self):
        url = "http://static-maps.yandex.ru/1.x/"
        params = {'ll': self.coords, 'z': f'{self.z}', 'l': 'map'}
        response = requests.get(url, params=params)

        if not response:
            print("Ошибка выполнения запроса")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.setImage()

    def setImage(self):
        self.pix = QPixmap(self.map_file)
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
