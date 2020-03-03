import os
import sys
from math import radians, sin, sqrt, asin, cos

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5 import uic, Qt
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class Maps(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('des.ui', self)
        self.lbl.setFocus()
        self.x = '55.753215'
        self.y = '37.622504'
        self.z = '5'
        self.l = 'map'
        self.photo = 'map.png'
        self.text_met = 'pm2rdm'
        self.metka = ''
        self.is_index = False
        self.resp = ''
        self.schema.clicked.connect(lambda: self.change_type_map('map'))
        self.sput.clicked.connect(lambda: self.change_type_map('sat'))
        self.gibrid.clicked.connect(lambda: self.change_type_map('sat,skl'))
        self.search1.clicked.connect(self.search)
        self.sbros.clicked.connect(self.clear_search)
        self.index1.stateChanged.connect(self.add_index)
        self.getImage()

    def add_index(self):
        if not self.is_index:
            self.is_index = True
            if self.resp:
                text = self.address1.toPlainText()
                text += '\nПочтовый индекс: '
                index = self.resp['response']['GeoObjectCollection']['featureMember'][0][
                    'GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
                text += index
                self.address1.setPlainText(text)
        else:
            self.is_index = False
            text = self.address1.toPlainText()
            text = text.split('\n')
            text = '\n'.join(text[:-1])
            self.address1.setPlainText(text)

    def clear_search(self):
        self.lbl.setFocus()
        self.metka = ''
        self.address1.setPlainText('')
        self.getImage()

    def search(self):
        self.lbl.setFocus()
        text = self.led.text()
        url = 'http://geocode-maps.yandex.ru/1.x/'
        params = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'format': 'json',
            'geocode': f'{text}'
        }
        response = requests.get(url, params=params)
        if not response:
            print("Ошибка выполнения запроса")
            print("Http статус:", response.status_code, "(", response.reason, ")")
        else:
            try:
                response = response.json()
                self.resp = response
                address = response['response']['GeoObjectCollection'][
                    'featureMember'][0]['GeoObject']['metaDataProperty'][
                    'GeocoderMetaData']['text']
                if self.is_index:
                    address += '\nПочтовый индекс: '
                    index = response['response']['GeoObjectCollection']['featureMember'][0][
                        'GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
                    print(index)
                    address += index
                self.address1.setPlainText(address)
                coords = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                    'Point']['pos'].split()
                self.x = coords[1]
                self.y = coords[0]
                self.metka = f'{self.y},{self.x},{self.text_met}'
                self.getImage()
            except BaseException:
                pass

    def change_type_map(self, type1):
        self.l = type1
        if self.l != 'map':
            self.photo = 'map.jpg'
        else:
            self.photo = 'map.png'
        self.getImage()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x_m = event.pos().x()
            y_m = event.pos().y()
            if 0 <= x_m < 600 and 0 <= y_m < 450:
                x = (x_m - 300) * 360 / 2 ** (int(self.z) + 8)
                y = (y_m - 225) * 230 / 2 ** (int(self.z) + 8)
                self.x = str(float(self.x) - y)
                self.y = str(x + float(self.y))
                self.metka = f'{self.y},{self.x},{self.text_met}'
                self.getImage()
                url = 'http://geocode-maps.yandex.ru/1.x/'
                params = {
                    'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                    'format': 'json',
                    'geocode': f'{self.y},{self.x}'
                }
                response = requests.get(url, params=params)
                if not response:
                    print("Ошибка выполнения запроса")
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                else:
                    try:
                        response = response.json()
                        self.resp = response
                        address = response['response']['GeoObjectCollection'][
                            'featureMember'][0]['GeoObject']['metaDataProperty'][
                            'GeocoderMetaData']['text']
                        if self.is_index:
                            address += '\nПочтовый индекс: '
                            index = response['response']['GeoObjectCollection']['featureMember'][0][
                                'GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
                            print(index)
                            address += index
                        self.address1.setPlainText(address)
                    except BaseException:
                        pass
        elif event.button() == Qt.RightButton:
            x_m = event.pos().x()
            y_m = event.pos().y()
            if 0 <= x_m < 600 and 0 <= y_m < 450:
                x = (x_m - 300) * 360 / 2 ** (int(self.z) + 8)
                y = (y_m - 225) * 230 / 2 ** (int(self.z) + 8)
                self.x = str(float(self.x) - y)
                self.y = str(x + float(self.y))
                self.metka = f'{self.y},{self.x},{self.text_met}'
                self.organisation()

    def organisation(self):
        url = 'http://geocode-maps.yandex.ru/1.x/'
        params = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'format': 'json',
            'geocode': f'{self.y},{self.x}'
        }
        response = requests.get(url, params=params)
        if not response:
            print("Ошибка выполнения запроса")
            print("Http статус:", response.status_code, "(", response.reason, ")")
        else:
            try:
                response = response.json()
                self.resp = response
                address = response['response']['GeoObjectCollection'][
                    'featureMember'][0]['GeoObject']['metaDataProperty'][
                    'GeocoderMetaData']['text']
                print(address)
            except BaseException:
                pass

        url = "https://search-maps.yandex.ru/v1/"
        params = {
            "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
            'text': address,
            "lang": "ru_RU",
            'spn': '0.005,0.005',
            "type": "biz",
            'results': 10
        }
        response = requests.get(url, params=params)
        response = response.json()
        print(response)
        if not response:
            print("Ошибка выполнения запроса")
            print("Http статус:", response.status_code, "(", response.reason, ")")
        else:
            min1 = 50
            min_org = ''
            for i in range(10):
                try:
                    org = response["features"][i]
                    y, x = org["geometry"]["coordinates"]
                    s = self.get_long([float(self.y), float(self.x)], [y, x])
                    print(s, org)
                    if min1 > s:
                        min1 = s
                        min_org = org
                except IndexError:
                    pass
            try:
                print(min1, min_org, sep='\n')
                address = min_org['properties']['name']
                address = address + '\n' + min_org['properties']['description']
                self.address1.setPlainText(address)
                self.y, self.x = min_org['geometry']['coordinates']
                self.y, self.x = str(self.y), str(self.x)
                self.metka = f'{self.y},{self.x},{self.text_met}'
                self.getImage()
            except BaseException:
                pass

    def get_long(self, a, b):
        degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
        a_lon, a_lat = a
        b_lon, b_lat = b

        # Берем среднюю по широте точку и считаем коэффициент для нее.
        radians_lattitude = radians((a_lat + b_lat) / 2.)
        lat_lon_factor = cos(radians_lattitude)

        # Вычисляем смещения в метрах по вертикали и горизонтали.
        dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
        dy = abs(a_lat - b_lat) * degree_to_meters_factor

        # Вычисляем расстояние между точками.
        distance = sqrt(dx * dx + dy * dy)

        return distance

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

        if event.key() == QtCore.Qt.Key_Down:
            self.shift = 450 * 180 / 2 ** (int(self.z) + 8)
            if float(self.x) - self.shift > -90:
                self.x = str(float(self.x) - self.shift)
                self.getImage()

        if event.key() == QtCore.Qt.Key_Left:
            self.shift = 600 * 360 / 2 ** (int(self.z) + 8)
            if float(self.y) - self.shift > -180:
                self.y = str(float(self.y) - self.shift)
                self.getImage()

        if event.key() == QtCore.Qt.Key_Right:
            self.shift = 600 * 360 / 2 ** (int(self.z) + 8)
            if float(self.y) + self.shift < 180:
                self.y = str(float(self.y) + self.shift)
                self.getImage()

    def getImage(self):
        url = "http://static-maps.yandex.ru/1.x/"
        params = {
            'll': f'{self.y},{self.x}',
            'z': f'{self.z}',
            'l': self.l,
            'pt': self.metka,
            'size': '600,450'}
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
