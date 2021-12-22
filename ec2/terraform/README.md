## IoC for deployment of ec2 with ssh and rdp connection execution


### Workbook:
~~~
# Destroys env if exists and creates a new one.
python execute_tf_commands.py
~~~
In addition to the provisioning functionality above, the following arguments will automatically open an SSH terminal or an RDP connection window right from your Windows machine upon successful execution of the provisioning steps:
~~~
python execute_tf_commands.py ssh
python execute_tf_commands.py rpd
~~~


### Prerequisites:
- place your pem key in the external directory.
- fill dev.tfvars with appropriate definitions pertaining to your AWS environment and configuration.
