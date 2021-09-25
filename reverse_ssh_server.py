import paramiko
import socket
import threading
def start_channel():
    # Define authentication key
    key = paramiko.RSAKey(filename='server_key.key')
    # authenticate client
    auth_sock = socket.socket()
    auth_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # stop the os from yelling about the port
    auth_sock.bind(('0.0.0.0', 22))
    auth_sock.listen()
    client_socket, client_address = auth_sock.accept()
    print('connection requested: {}'.format(client_address))
    # start server
    ssh_server = paramiko.Transport(client_socket)
    ssh_server.add_server_key(key)
    ssh_server.start_server(server=Server())
    # accept client
    channel = ssh_server.accept()
    print('connection accepted: {}'.format(client_address))
    return channel
class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    username = 'aryehshebson'
    password = 'pass'

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == self.username) and (password == self.password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True
channel = start_channel()
#start coversation
print(channel.recv(1024).decode(),end='')
while True:
    try:
        cmd = input()
        channel.send(cmd)
        if cmd == 'exit':
            print('exiting...')
            break
        print(channel.recv(1024).decode(),end='')
    except socket.error:
        print('socket broke')
        print('reconnecting...')
        channel = start_channel()
        print(channel.recv(1024).decode(), end='')







