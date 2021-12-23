import os
import subprocess
import sys
from time import sleep


def create_environment_if_not_exists():
    subprocess.run('terraform init -upgrade')
    # subprocess.run('terraform plan')
    subprocess.run('terraform apply --var-file="dev.tfvars" -auto-approve')


def destroy_environment_if_exists():
    subprocess.run('terraform destroy -auto-approve --var-file="dev.tfvars"')


def open_ssh_connection_to_ec2():
    print('\nChecking if local pem key exists...')
    pem_key_location = get_pem_key_location()
    print('Waiting for a few seconds to allow SSH service to start.')  # In case EC2 was just created.
    sleep(10)
    ec2_ip = get_value_from_output('ec2_public_ip')
    ec2_user = get_value_from_output('ec2_username')
    command = f'ssh -i "{pem_key_location}" -o StrictHostKeyChecking=no {ec2_user}@{ec2_ip}'
    print(f'Opening SSH connection terminal to host {ec2_ip}.')
    os.system(f'start /wait cmd /c {command}')
    print(f'SSH connection closed.')


def get_pem_key_location():
    external_directory = get_value_from_output('external_directory')
    with open('dev.tfvars', 'r') as f:
        key_file = next(iter([line.rstrip().split('"')[1] for line in f.readlines() if 'pem_key_file_name' in line]), None)
    if not external_directory or not key_file:
        print(f'Missing external_directory or pem_key_file_name definitions within your tfvars file.'
              f' Check that variables are defined correctly before re-running. Exiting.')
        sys.exit(1)
    if key_file not in os.listdir(external_directory):
        print(f'No key was found under {external_directory}/{key_file} as per your tfvars file definitions.'
              f' Check the existence of the file before re-running. Exiting.')
        sys.exit(1)
    return f'{external_directory}/{key_file}'


def open_rdp_connection_to_ec2():
    ec2_ip = get_value_from_output('ec2_public_ip')
    command = f'mstsc /v:{ec2_ip}'
    print(f'\nOpening RDP connection window to host {ec2_ip}.')
    os.system(f'start /wait cmd /c {command}')
    print(f'RDP connection closed.')


def get_value_from_output(output_param):
    return subprocess.check_output(f'terraform output {output_param}').decode('utf-8').replace('"', '').rstrip()


if __name__ == '__main__':
    destroy_environment_if_exists()
    create_environment_if_not_exists()

    if len(sys.argv) > 1:
        connection = sys.argv[1]
        if connection == 'ssh':
            open_ssh_connection_to_ec2()
        elif connection == 'rdp':
            open_rdp_connection_to_ec2()
        else:
            print(f'Parameter "{connection}" is not a valid entry. Acceptable inputs are "ssh" or "rdp".')
