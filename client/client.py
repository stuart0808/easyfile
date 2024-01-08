import argparse
import socket
import os
from tqdm import tqdm
import json
from datetime import datetime
import humanfriendly

version = '1.0.6'

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def print_status(status, color, ifprint = True):
    if ifprint == False:
        return
    ip_add = get_ip_address()
    
    colors = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m"
    }
    
    if color.lower() not in colors:
        print("Invalid color!")
        return
    
    print(f"{colors[color.lower()]}" + f"[{datetime.now()}] {ip_add}:8765 {status}" + f"{colors['reset']}")
    with open('severlog.txt', 'a') as file:
        file.write(f"[{datetime.now()}] {ip_add}:8765 {status}")
        file.write('\n')

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, choices=['list', 'upload', 'download', 'version', 'login'], help='list, upload, download, version, login')
parser.add_argument('--file_path', type=str, help='file path')
parser.add_argument('--file_name', type=str, help='file name')
args = parser.parse_args()

IP = '172.26.204.165'

def upload(file_path):
    # 处理上传操作
    try:
        # 创建TCP Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, 8765))
        client_socket.send("upload".encode())
        print_status(f"发送指令:upload", "reset")
        confirmation = client_socket.recv(1024).decode()
        # 判断文件是否存在
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            # 发送文件名到服务器
            client_socket.send(file_name.encode('utf-8'))
            # 等待接收确认消息
            confirmation = client_socket.recv(1024).decode()
            if confirmation == "ready":
                # 打开文件并上传
                with open(file_path, 'rb') as f:
                    # 获取文件大小
                    file_size = os.path.getsize(file_path)
                    progress_bar = tqdm(f, total=file_size, unit='B', unit_scale=True)
                    for data in f:
                        client_socket.send(data)
                        progress_bar.update(len(data))
                    progress_bar.close()
                print_status(f"指令结束:upload:文件上传完成", "reset")
            else:
                print_status(f"指令结束:upload:文件上传失败", "red")
        else:
            print_status(f"指令结束:upload:文件不存在", "red")
    except Exception as e:
        print_status(f"连接出错:{e}", "red")

def download(cloud_file_name, cloud_file_size, path):
    # 将文件大小转换为字节数
    file_size_bytes = humanfriendly.parse_size(cloud_file_size)
    path = path + '/' + cloud_file_name
    # 处理下载操作
    try:
        # 创建TCP Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, 8765))
        client_socket.send("download".encode())
        print_status(f"发送指令:download", "reset")
        confirmation = client_socket.recv(1024).decode()
        client_socket.send(cloud_file_name.encode('utf-8'))
        # 接收服务器的响应
        confirmation = client_socket.recv(1024).decode()
        
        if confirmation == "ready":
            # 发送文件名给服务器
            # 创建文件并接收数据
            with open(path, 'wb') as f, tqdm(total=file_size_bytes, unit='B', unit_scale=True) as pbar:
                while True:
                    data = client_socket.recv(1024)
                    if data == b'':
                        break
                    f.write(data)
                    pbar.update(len(data))
            print_status(f"指令结束:download:文件接收完成", "reset")
        else:
            print_status(f"指令结束:download:文件不存在", "red")
    except Exception as e:
        print_status(f"连接出错:{e}", "red")

def list():
    # 处理连接服务器操作
    try:
        # 创建TCP Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, 8765))
        client_socket.send("list".encode())
        print_status(f"发送指令:list", "reset", False)
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
        # 关闭Socket连接
        client_socket.close()
        print_status(f"指令结束:list:文件列表已接收", "reset", False)
        return file_list
    except Exception as e:
        print_status(f"连接出错:{e}", "red", False)
        return -1

def update(): 
    try:
        # 创建TCP Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, 8765))
        client_socket.send("version".encode())
        print_status(f"发送指令:version", "reset")
        # 接收服务器的响应
        confirmation = client_socket.recv(1024).decode()
        client_socket.send(version.encode('utf-8'))
        confirmation = client_socket.recv(1024).decode()
        if confirmation == "ready":
            print_status(f"指令结束:version:已是最新版本", "green")
        if confirmation == "new":
            print_status(f"指令结束:version:有新版本", "red")
    except Exception as e:
        print_status(f"连接出错:{e}", "red")
