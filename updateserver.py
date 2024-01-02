import socket

HOST = '172.26.204.165'  # 本地主机IP
PORT = 9090  # 端口号

def send_file(conn, filename):
    with open(filename, 'rb') as f:
        data = f.read(1024)
        while data:
            conn.send(data)
            data = f.read(1024)

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print('等待客户端连接...')

    conn, addr = server_socket.accept()
    print(f'已连接: {addr}')

    filename = 'D:\\code_container\\easyfile\\main.py'  # 要发送的文件路径
    send_file(conn, filename)
    rec = conn.recv(1024).decode()
    print(rec)
    filename = 'D:\\code_container\\easyfile\\login.py'  # 要发送的文件路径
    send_file(conn, filename)
    rec = conn.recv(1024).decode()
    print(rec)
    conn.close()
    server_socket.close()

if __name__ == '__main__':
    while True:
        run_server()
