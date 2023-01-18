import os
from datetime import datetime

import requests
from PyQt6 import QtWidgets, QtCore
from clientui import Ui_MainWindow
from dotenv import load_dotenv

load_dotenv()

MESSENGER_HOST = os.getenv("MESSENGER_HOST") or "http://127.0.0.1:5000"


class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._host = MESSENGER_HOST
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
                self._host + "/messages", params={"after": self.after}
            )
        except Exception as e:
            print(e)
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
                self._host + "/send", json={"name": name, "text": text}
            )
        except Exception as e:
            print(e)
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
window = Messenger()
window.show()
app.exec()
