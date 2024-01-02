from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import os
import sys
import json
from PyQt5.QtWidgets import QLabel, QMainWindow, QTreeView, QFileSystemModel, QTableWidget,QTableWidgetItem, QDialog
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QMessageBox, QProgressBar
from tqdm import tqdm



class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        
        self.username = QLabel(self)
        self.username.setText("Username:")
        self.username.move(10, 10)
        
        self.username_e = QLineEdit(self)
        self.username_e.setGeometry(150, 10, 200, 20)

        self.password = QLabel(self)
        self.password.setText("Password:")
        self.password.move(10, 40)

        self.password_e = QLineEdit(self)
        self.password_e.setEchoMode(QLineEdit.Password)
        self.password_e.setGeometry(150, 40, 200, 20)
        
        self.verify_button = QPushButton("Verify", self)
        self.verify_button.setGeometry(10, 70, 120, 30)
        self.verify_button.clicked.connect(self.verifyActivation)
        
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setGeometry(150, 70, 120, 30)
        self.cancel_button.clicked.connect(self.reject)

    def accept(self) -> None:
        return super().accept()

    def reject(self) -> None:
        return super().reject()
    
    def verifyActivation(self):
        # 创建TCP socket，连接服务器
        server_address = ('172.26.204.165', 8765)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        client_socket.send("login".encode())
        response = client_socket.recv(1024).decode()
        print(response)

        # 构建请求字典对象
        request = {
            'username': self.username_e.text(),
            'password': self.password_e.text()
        }

        # 发送请求给服务器
        request = json.dumps(request).encode()
        client_socket.send(request)

        # 接收服务器返回的验证结果
        response = client_socket.recv(1024).decode()
        response = json.loads(response)

        # 处理验证结果
        if response['status'] == 'success':
            QMessageBox.information(self, 'Login', response['message'])
            self.accept()
        else:
            QMessageBox.warning(self, 'Login', response['message'])

        # 关闭socket连接
        client_socket.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginDialog = LoginDialog()
    loginDialog.show()

    sys.exit(app.exec_())