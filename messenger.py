from datetime import datetime

import requests
from PyQt6 import QtWidgets, QtCore
from clientui import Ui_MainWindow


class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, host="127.0.0.1:5000"):
        super().__init__()
        self.setupUi(self)

        self.host = host

        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def print_message(self, message):
        dt = datetime.fromtimestamp(message["time"])
        dt_str = dt.strftime("%d %b %H:%M:%S")
        self.textBrowser.append(dt_str + " " + message["name"])
        self.textBrowser.append(message["text"])
        self.textBrowser.append("")

    def get_messages(self):
        try:
            response = requests.get(
                "https://" + self.host + "/messages?", params={"after": self.after}
            )
        except:
            return

        messages = response.json()["messages"]
        for message in messages:
            self.print_message(message)
            self.after = message["time"]

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        try:
            response = requests.post(
                "https://" + self.host + "/send", json={"name": name, "text": text}
            )
        except:
            self.textBrowser.append("Сервер недоступен")
            self.textBrowser.append("Попробуйте еще раз")
            self.textBrowser.append("")
            return

        if response.status_code != 200:
            self.textBrowser.append(
                "Имя и текст не должны быть пустыми. Текст не должен привышать 1000 символов."
            )
            self.textBrowser.append("")
            return

        self.textEdit.clear()


app = QtWidgets.QApplication([])
window = Messenger("6356-31-128-252-135.eu.ngrok.io")
window.show()
app.exec()
