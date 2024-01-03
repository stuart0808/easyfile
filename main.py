from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import os
import sys
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from PyQt5.QtWidgets import QLabel, QMainWindow, QTreeView, QFileSystemModel, QTableWidget,QTableWidgetItem, QDialog
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QMessageBox, QProgressBar
from login import LoginDialog
from client import upload, download, list, update
from threading import Thread
from PyQt5.QtCore import QThread, QRunnable, pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication

version = '1.0.6'

class WorkThread(QThread):
    '''
    operation:
    =='1' UPLOAD
    =='2' DOWNLOAD
    =='3' LIST
    =='4' VERSION
    '''
    def __init__(self, arg1 = None, arg2 = None, operation = 0):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.operation = operation
    
    def run(self):
        if self.operation == '1':
            self.handleUpload()
        elif self.operation == '2':
            self.handleDownload()
        elif self.operation == '3':
            self.showCloudFiles()
        else:
            pass


    def handleUpload(self):
        # 在子线程中执行的操作
        upload(self.arg1)
        print("Executing handleUpload in the worker thread")
    def handleDownload(self):
        download(self.arg1, self.arg2)
        print("Executing handleDownload in the worker thread")
    def showCloudFiles(self):
        list()

class MainWindow(QMainWindow):
    refresh_list = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_list.emit)
        self.timer.start(5000)  # 5000 毫秒，即 5 秒

        self.refresh_list.connect(self.showCloudFiles)
        self.file_path = 'example.txt'
        self.cloud_file_name = 'example.txt'
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
        self.actionRefresh.triggered.connect(self.showCloudFiles)
        self.actionConnect_to_server.triggered.connect(self.showCloudFiles)
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
    
    # def handleUpload(self):
    #     # 处理上传操作
    #     upload(self.file_path)

    def handleUpload(self):
        # 处理上传操作
        self.upthread = WorkThread(self.file_path, None, '1')
        self.upthread.start()

    def handleDownload(self):
        # 处理下载操作
        self.downthread = WorkThread(self.cloud_file_name, self.cloud_file_size, '2')
        self.downthread.start()


    def showCloudFiles(self):
        self.listthread = WorkThread(None, None, '3')
        self.listthread.start()
        file_list = list()
        if file_list != -1:
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

    def handleUpdate(self):
        # 处理检查更新操作
        update()
    
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
        self.cloud_file_size = self.cloudfile.item(index.row(), 1).text()
        print(self.cloud_file_name)
        print(self.cloud_file_size)
        # 在这里处理选中文件的路径


        
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # 检查本地是否存在保存的用户名和密码
    if os.path.isfile("credentials.txt"):
        with open("credentials.txt", "r") as f:
            credentials = f.read().split(",")
            if len(credentials) == 2:
                username, password = credentials
                loginDialog = LoginDialog()
                loginDialog.username_e.setText(username)
                loginDialog.password_e.setText(password)
            else:
                loginDialog = LoginDialog()
    else:
        loginDialog = LoginDialog()
    if loginDialog.exec_() == QDialog.Accepted:
        mainWindow = MainWindow()
        mainWindow.show()
        try:
            # 创建TCP Socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((mainWindow.ip, 8765))
            client_socket.send("version".encode())
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
