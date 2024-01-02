import socket
import os
import datetime
import json

# 指定要返回文件信息的文件夹路径
folder_path = 'D:\\share_folder'
ip_add = '172.26.204.165'
sever_ver = "1.0.0"
# 创建TCP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip_add, 8765))
server_socket.listen(5)

print('等待客户端连接...')

while True:
    # 接受客户端连接
    client_socket, address = server_socket.accept()
    print('客户端已连接:', address)
    command = client_socket.recv(1024).decode()
    print("接收到指令：", command)
    if command == "l":
        file_list = []

        # 获取文件夹中所有文件的信息
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            file_size = os.path.getsize(file_path)
            modified_time = os.path.getmtime(file_path)
            modified_time = datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
            file_info = (filename, file_size, modified_time)
            file_list.append(file_info)

        json_data = json.dumps(file_list)
        print(json_data)
        # 将文件信息发送给客户端
        print(str(len(json_data)))
        client_socket.send(str(len(json_data)).encode())
        client_socket.send((json_data).encode())

        print('文件信息已发送给客户端')

        # 关闭客户端连接
        client_socket.close()
    elif command == "u":
        # 发送确认消息
        client_socket.send("ready".encode())
        print("等待文件传输...")
        # 接收客户端上传的文件
        file_name = client_socket.recv(1024).decode()
        if file_name:
            # 下载文件
            with open(f"D:\\share_folder\\{file_name}", 'wb') as f:
                while True:
                    data = client_socket.recv(1024)
                    if data == b'':
                        break
                    f.write(data)
            print("文件接收完成")
        else:
            print("文件名为空")
        client_socket.close()
    elif command == "d":
        client_socket.send("OK".encode())
        # 接收客户端要下载的文件名
        file_name = client_socket.recv(1024).decode()
        print("接收到文件名：", file_name)
        if file_name:
            # 判断文件是否存在
            if os.path.exists(f"D:\\share_folder\\{file_name}"):
                client_socket.send("ready".encode())
                # 发送文件数据
                with open(f"D:\\share_folder\\{file_name}", 'rb') as f:
                    for data in f:
                        client_socket.send(data)
                print("文件发送完成")
            else:
                client_socket.send("fail".encode())
                print("文件不存在")
        else:
            print("文件名为空")
        client_socket.close()
    elif command == "num":
        client_socket.send("Checking".encode())
        client_ver = client_socket.recv(1024).decode()
        if client_ver == sever_ver:
            client_socket.send("ready".encode())
            print("ready")
        else:
            client_socket.send("new".encode())
            print("new")
