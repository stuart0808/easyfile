import socket

HOST = '172.26.204.165'  # 服务端IP
PORT = 9090  # 端口号

def save_file(conn, filename):
    with open(filename, 'wb') as f:
        data = conn.recv(1024)
        while data:
            f.write(data)
            data = conn.recv(1024)

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    filename = 'main.py'  # 下载文件保存的路径和文件名
    save_file(client_socket, filename)

    print('文件下载已完成')

    client_socket.close()

if __name__ == '__main__':
    run_client()
