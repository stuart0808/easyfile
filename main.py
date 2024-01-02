from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import os
import sys
import json
from PyQt5.QtWidgets import QLabel, QMainWindow, QTreeView, QFileSystemModel, QTableWidget,QTableWidgetItem, QDialog
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QMessageBox, QProgressBar
from tqdm import tqdm
from login import LoginDialog

version = '1.0.2'
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.ip = '172.26.204.165'

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(886, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.local_flie = QFileSystemModel()
        self.localfile = QtWidgets.QTreeView(self.centralwidget)
        self.localfile.setGeometry(QtCore.QRect(10, 50, 301, 491))
        self.localfile.setObjectName("localfile")
        self.localFlie()

        self.TitleLabel = QLabel(self.centralwidget)
        self.TitleLabel.setGeometry(QtCore.QRect(10, 10, 124, 38))
        self.TitleLabel.setObjectName("TitleLabel")
        self.upload = QtWidgets.QPushButton(self.centralwidget)
        self.upload.setGeometry(QtCore.QRect(630, 50, 75, 24))
        self.upload.setObjectName("upload")
        self.cloudfile = QtWidgets.QTableWidget(self.centralwidget)
        self.cloudfile.setGeometry(QtCore.QRect(320, 50, 301, 491))
        self.cloudfile.setObjectName("cloudfile")
        self.TitleLabel_2 = QLabel(self.centralwidget)
        self.TitleLabel_2.setGeometry(QtCore.QRect(320, 10, 131, 38))
        self.TitleLabel_2.setObjectName("TitleLabel_2")
        self.download = QtWidgets.QPushButton(self.centralwidget)
        self.download.setGeometry(QtCore.QRect(630, 80, 75, 24))
        self.download.setObjectName("download")
        self.select = QtWidgets.QPushButton(self.centralwidget)
        self.select.setGeometry(QtCore.QRect(630, 110, 75, 24))
        self.select.setObjectName("select")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 886, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuConnect = QtWidgets.QMenu(self.menubar)
        self.menuConnect.setObjectName("menuConnect")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionUpload = QtWidgets.QAction(self)
        self.actionUpload.setObjectName("actionUpload")
        self.actionRefresh = QtWidgets.QAction(self)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionCheck_for_update = QtWidgets.QAction(self)
        self.actionCheck_for_update.setObjectName("actionCheck_for_update")
        self.actionConnect_to_server = QtWidgets.QAction(self)
        self.actionConnect_to_server.setObjectName("actionConnect_to_server")
        self.menuFile.addAction(self.actionUpload)
        self.menuFile.addAction(self.actionRefresh)
        self.menuConnect.addAction(self.actionConnect_to_server)
        self.menuSettings.addAction(self.actionCheck_for_update)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConnect.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi()
        self.upload.clicked.connect(self.handleUpload)
        self.download.clicked.connect(self.handleDownload)
        self.select.clicked.connect(self.handleSelect)
        self.actionUpload.triggered.connect(self.handleUpload)
        self.actionRefresh.triggered.connect(self.handleRefresh)
        self.actionConnect_to_server.triggered.connect(self.handleConnect)
        self.actionCheck_for_update.triggered.connect(self.handleUpdate)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TitleLabel.setText(_translate("MainWindow", "Local File"))
        self.upload.setText(_translate("MainWindow", "Upload"))
        self.TitleLabel_2.setText(_translate("MainWindow", "Cloud File"))
        self.download.setText(_translate("MainWindow", "Download"))
        self.select.setText(_translate("MainWindow", "Select"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuConnect.setTitle(_translate("MainWindow", "Connect"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionUpload.setText(_translate("MainWindow", "Upload"))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionCheck_for_update.setText(_translate("MainWindow", "Check for update"))
        self.actionConnect_to_server.setText(_translate("MainWindow", "Connect to server"))
    
    def handleSelect(self):
        # 文件筛选器
        self.file_path, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*);;Text Files (*.txt)")
        print(self.file_path, filetype)
        self.handleUpload()

    def handleUpload(self):
        # 处理上传操作
        print('upload')
        try:
            # 创建TCP Socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip, 8765))
            client_socket.send("u".encode())
            confirmation = client_socket.recv(1024).decode()
            # 判断文件是否存在
            if os.path.exists(self.file_path):
                file_name = os.path.basename(self.file_path)
                print(file_name)
                # 发送文件名到服务器
                client_socket.send(file_name.encode('utf-8'))
                print("发送文件名成功")
                # 等待接收确认消息
                confirmation = client_socket.recv(1024).decode()
                print(confirmation)
                if confirmation == "ready":

                    # 打开文件并上传
                    with open(self.file_path, 'rb') as f:
                        # 获取文件大小
                        file_size = os.path.getsize(self.file_path)
                        progress_bar = tqdm(f, total=file_size, unit='B', unit_scale=True)
                        for data in f:
                            client_socket.send(data)
                            progress_bar.update(len(data))
                        progress_bar.close()
                    print("文件上传成功")
                else:
                    print("文件上传失败")
            else:
                print("文件不存在")
        except Exception as e:
            print('连接出错:', e)
    
    def handleDownload(self):
        # 处理下载操作
        print('download')
        try:
            # 创建TCP Socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip, 8765))
            client_socket.send("d".encode())
            confirmation = client_socket.recv(1024).decode()
            print(confirmation)
            client_socket.send(self.cloud_file_name.encode('utf-8'))
            # 接收服务器的响应
            confirmation = client_socket.recv(1024).decode()
            print(confirmation)
            
            if confirmation == "ready":
                # 发送文件名给服务器
                # 创建文件并接收数据
                with open(self.cloud_file_name, 'wb') as f:
                    while True:
                        data = client_socket.recv(1024)
                        if data == b'':
                            break
                        f.write(data)
                print("文件接收完成")
            else:
                print("文件不存在")
        except Exception as e:
            print('连接出错:', e)

    def handleRefresh(self):
        # 处理刷新操作
        print('refresh')
        pass

    def handleConnect(self):
        # 处理连接服务器操作
        try:
            # 创建TCP Socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip, 8765))
            client_socket.send("l".encode())
            len_json = int(client_socket.recv(1024).decode())

            file_info = ""

            for row in range(round(len_json+1024/1024)):
                # 接收文件信息

                temp = client_socket.recv(1024).decode()
                file_info += temp

            # 解析JSON数据为Python对象
            data = json.loads(file_info)

            # 创建空的二维列表
            file_list = []

            # 遍历每个子列表
            for sublist in data:
                # 将子列表添加到二维列表
                file_list.append(sublist)

            print(file_list)
            print(len(file_list))
            
            # 设置表格控件的行列数
            self.cloudfile.setRowCount(len(file_list))
            self.cloudfile.setColumnCount(3)
            self.cloudfile.setHorizontalHeaderLabels(['文件名', '大小', '修改时间'])
            self.cloudfile.clicked.connect(self.cloudfile_handle_click)

            
            for row in range(len(file_list)):
                file_info = file_list[row]
                # 将文件信息显示在表格中
                self.cloudfile.setItem(row, 0, QTableWidgetItem(file_info[0]))
                self.cloudfile.setItem(row, 1, QTableWidgetItem(self.convert_file_size(file_info[1])))
                self.cloudfile.setItem(row, 2, QTableWidgetItem(file_info[2]))

            # 关闭Socket连接
            client_socket.close()

        except Exception as e:
            print('连接出错:', e)

    def handleUpdate(self):
        # 处理检查更新操作
        print('update')
        pass
    
    def localFlie(self):
        # 处理本地文件
        
        self.local_flie.setRootPath("")
        self.localfile.setModel(self.local_flie)
        self.localfile.setRootIndex(self.local_flie.index(os.path.expanduser("~"))) # 设置根目录为用户主目录
        self.localfile.clicked.connect(self.local_flie_handle_click)
    
    def local_flie_handle_click(self, index):
        self.file_path = self.local_flie.filePath(index)
        
        if os.path.isfile(self.file_path):
            print(self.file_path)  # 在这里处理选中文件的路径

    def convert_file_size(self, file_size):
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0

        while file_size >= 1024 and unit_index < len(units)-1:
            file_size /= 1024
            unit_index += 1

        return "{:.2f} {}".format(file_size, units[unit_index])
    
    def cloudfile_handle_click(self, index):
        self.cloud_file_name = self.cloudfile.item(index.row(), 0).text()
        print(self.cloud_file_name)
        # 在这里处理选中文件的路径


        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginDialog = LoginDialog()
    if loginDialog.exec_() == QDialog.Accepted:
        print("Accepted")
        mainWindow = MainWindow()
        mainWindow.show()
        try:
            # 创建TCP Socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((mainWindow.ip, 8765))
            client_socket.send("num".encode())
            # 接收服务器的响应
            confirmation = client_socket.recv(1024).decode()
            client_socket.send(version.encode('utf-8'))
            confirmation = client_socket.recv(1024).decode()
            if confirmation == "ready":
                print("已是最新版本")
            if confirmation == "new":
                print("有新版本")
                #关闭窗口
                sys.exit(1)
        except Exception as e:
            print('连接出错:', e)
        sys.exit(app.exec_())
    else:
        print("Rejected")
        sys.exit(1)
