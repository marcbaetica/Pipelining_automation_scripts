import subprocess


# subprocess.run('terraform init'
subprocess.run('terraform init -upgrade')
# subprocess.run('terraform plan')
subprocess.run('terraform apply -auto-approve')
