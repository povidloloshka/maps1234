import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import requests
from geo import get_сoordinates


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('mainwindow.ui', self)
        self.api_server = 'http://static-maps.yandex.ru/1.x/'
        self.map_zoom = 8
        self.delta = 0.1
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 'map'
        self.refresh_map()
        self.search.clicked.connect(self.set_search)
        self.gibrid.clicked.connect(self.set_gibrid)
        self.sputnik.clicked.connect(self.set_satellite)
        self.scheme.clicked.connect(self.set_map)

    def refresh_map(self):
        map_params = {
            'll': ','.join(map(str, self.map_ll)),
            'l': self.map_l,
            'z': self.map_zoom
        }
        response = requests.get(self.api_server, params=map_params)
        if not response:
            print(f'Ошибка выполнения запроса: HTTP статус: {response.status_code} ({response.reason})')

        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)
        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.map.setPixmap(pixmap)

    def set_map(self):
        self.map_l = 'map'
        self.refresh_map()

    def set_gibrid(self):
        self.map_l = 'sat, skl'
        self.refresh_map()

    def set_satellite(self):
        self.map_l = 'sat'
        self.refresh_map()

    def set_search(self):
        long, lat = get_сoordinates(self.lineEdit.text())
        self.map_ll = (long, lat)
        self.refresh_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.map_zoom < 17:
            self.map_zoom += 1
        if event.key() == Qt.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if event.key() == Qt.Key_Left:
            self.map_ll[0] -= self.delta
        if event.key() == Qt.Key_Right:
            self.map_ll[0] += self.delta
        if event.key() == Qt.Key_Up:
            self.map_ll[1] += self.delta
        if event.key() == Qt.Key_Down:
            self.map_ll[1] -= self.delta
        self.refresh_map()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
