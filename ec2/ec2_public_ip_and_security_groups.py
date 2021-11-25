import boto3
import json
from pprintpp import pprint
from ec2.encoders.datetime_encoder import DatetimeEncoder


def get_ec2s_descriptions():
    ec2 = boto3.client('ec2', region_name='us-west-2')
    res = ec2.describe_instances()
    with open('descriptions.json', 'w') as f:
        f.write(json.dumps(res, cls=DatetimeEncoder))


def read_ec2s_descriptions():
    with open('descriptions.json', 'r') as f:
        return json.loads(f.read())


def extract_public_ip_and_sec_group(instance):
    instance = instance['Instances'][0]
    if len(instance['NetworkInterfaces']):
        if 'Association' in instance['NetworkInterfaces'][0]:
            return instance['NetworkInterfaces'][0]['Association']['PublicIp'], instance['SecurityGroups']
    return None, instance['SecurityGroups']


# get_ec2s_descriptions()
response = read_ec2s_descriptions()
# pprint(response)
instances = [instance for instance in response['Reservations']]
print(len(instances))

for instance in instances:
    ip, sec_groups = extract_public_ip_and_sec_group(instance)
    print(ip, str(sec_groups))


# Checking account and region names:
# alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]
# print(alias)
# ec2 = boto3.client('ec2', region_name='us-west-2')
# print(ec2.meta.region_name)
