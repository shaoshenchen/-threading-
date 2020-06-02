import socket
from PyQt5.QtWidgets import *
import ui
import sys
import threading


class Window(QWidget, ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.con)
        self.pushButton_2.clicked.connect(self.recv)
        self.pushButton_3.clicked.connect(self.send)
        self.pushButton_4.clicked.connect(self.cl)
        # socket里面默认的参数是数据流，要改成数据报
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def con(self):
        sender = self.lineEdit.text()
        QMessageBox.information(self, '连接服务器', '连接成功！')
        msg = "请求连接"
        self.s.sendto(sender.encode(), ("localhost", 8888))
        self.s.sendto("".encode(), ("localhost", 8888))
        self.s.sendto(msg.encode(), ("localhost", 8888))

    def send(self):
        sender = self.lineEdit.text()
        recipient = self.lineEdit_2.text()
        text = self.lineEdit_3.text()

        self.s.sendto(sender.encode(), ("localhost", 8888))
        self.s.sendto(recipient.encode(), ("localhost", 8888))
        self.s.sendto(text.encode(), ("localhost", 8888))

        self.textEdit.append('你：' + text)
        self.lineEdit_3.clear()

    def recv(self):
        sender = self.s.recv(1024)
        data = self.s.recv(1024)
        self.textEdit.append(sender.decode() + ": " + data.decode())

    def cl(self):
        self.textEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win1 = Window()
    win2 = Window()
    t1 = threading.Thread(target=win1.show())
    t2 = threading.Thread(target=win2.show())
    t1.start()
    t2.start()

    sys.exit(app.exec_())
