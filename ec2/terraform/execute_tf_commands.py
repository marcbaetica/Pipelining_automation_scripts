import os
import subprocess
from pprintpp import pprint
from time import sleep

def create_environment_if_not_exists_and_open_ssh():
    # subprocess.run('terraform init'
    subprocess.run('terraform init -upgrade')
    # subprocess.run('terraform plan')
    subprocess.run('terraform apply -auto-approve')

    print('Waiting for a few seconds to allow SSH service to start.')
    sleep(10)
    print('Opening SSH window.')
    ec2_ip = subprocess.check_output('terraform output -json ec2_public_ip').decode('utf-8').replace('"', '')
    command = f'ssh -i "Automation-Ohio.pem" -o StrictHostKeyChecking=no ubuntu@{ec2_ip}'
    os.system(f'start /wait cmd /c {command}')


def destroy_environment():
    subprocess.run('terraform destroy -auto-approve')


destroy_environment()  # Destroy if already exists.
create_environment_if_not_exists_and_open_ssh()
