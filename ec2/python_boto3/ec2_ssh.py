import os
import paramiko
import sys
from pprintpp import pprint
from dotenv import load_dotenv


load_dotenv()

OPENSSH_KEYS_PATH = os.getenv('OPENSSH_KEYS_PATH')
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASS = os.getenv('PASS')


sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sshClient.connect(HOST, username=USER, password=PASS, key_filename=OPENSSH_KEYS_PATH)

while True:
    print('\nEnter shell command:')
    command = input()  # cd .. && ls -la -> for different dir
    if command == 'exit':
        sshClient.close()
        break
    stdin, stdout, stderr = sshClient.exec_command(command)
    pprint(stdout.readlines())
