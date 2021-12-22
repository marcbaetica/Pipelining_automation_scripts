import os
import subprocess
import sys
from pprintpp import pprint
from time import sleep


def create_environment_if_not_exists_and_open_ssh():
    subprocess.run('terraform init -upgrade')
    # subprocess.run('terraform plan')
    subprocess.run('terraform apply --var-file="dev.tfvars" -auto-approve')


def destroy_environment_if_exists():
    subprocess.run('terraform destroy -auto-approve --var-file="dev.tfvars"')


def open_ssh_connection_to_ec2():
    print('Checking if pem key exists...')
    pem_key_location = get_pem_key_location()
    print('Waiting for a few seconds to allow SSH service to start.')  # In case EC2 was just created.
    sleep(10)
    print('Opening SSH window.')
    ec2_ip = subprocess.check_output('terraform output -json ec2_public_ip').decode('utf-8').replace('"', '')
    # TODO: Get username from either whoami or put in output and extract it from there.
    command = f'ssh -i "{pem_key_location}" -o StrictHostKeyChecking=no ubuntu@{ec2_ip}'
    os.system(f'start /wait cmd /c {command}')


def get_pem_key_location():  # TODO: Get external_directory from var and delete definition under tfvars file.
    with open('dev.tfvars', 'r') as f:
        data = [line.rstrip() for line in f.readlines()]
    if not any('external_directory' in line for line in data) or not any('pem_key_file_name' in line for line in data):
        print(f'Missing external_directory or pem_key_file_name definitions within your tfvars file.'
              f' Check that variables are defined correctly before re-running. Exiting.')
        sys.exit(1)
    external_directory = [line.split('"')[1] for line in data if 'external_directory' in line][0]
    key_file = [line.split('"')[1] for line in data if 'pem_key_file_name' in line][0]
    if key_file not in os.listdir(external_directory):
        print(f'No key was found under {external_directory}/{key_file} as per your tfvars file definitions.'
              f' Check the existence of the file before re-running. Exiting.')
        sys.exit(1)
    return f'{external_directory}/{key_file}'


if __name__ == '__main__':
    destroy_environment_if_exists()  # Destroy if already exists.
    create_environment_if_not_exists_and_open_ssh()

    open_ssh_connection_to_ec2()
