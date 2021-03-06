from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(800, 800)
        self.label1 = QLabel("Enter your host IP:", self)
        self.text = QLineEdit(self)
        self.text.move(10, 30)

        self.label3 = QLabel("api_key:", self)
        self.label3.move(10, 130)
        self.api_key = QLineEdit(self)
        self.api_key.move(10, 160)

        self.label4 = QLabel("ip:", self)
        self.label4.move(10, 190)
        self.ip = QLineEdit(self)
        self.ip.move(10, 220)


        self.label2 = QLabel("Answer:", self)
        self.label2.move(10, 60)
        self.button = QPushButton("Send", self)
        self.button.move(10, 90)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        hostname = self.text.text()
        api_key = self.api_key.text()
        ip = self.ip.text()

        if hostname == "":
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__query(hostname,api_key,ip)
            if res:
                self.label2.setText("https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" % (res["longitude"],res["latitude"]))
                webbrowser.open_new("https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" % (res["longitude"],res["latitude"]))
                self.label2.adjustSize()
                self.show()

    def __query(self, hostname, api_key, ip):
        url = "http://%s/ip/%s?key=%s" % (hostname, ip, api_key)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()
