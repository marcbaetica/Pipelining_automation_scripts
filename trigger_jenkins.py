import os
import requests as req
from dotenv import load_dotenv
from urllib.parse import urlencode


load_dotenv()

SERVER_URL = 'https://dsjenkins.trendmicro.com/automation'
JOB_BUILD = 'job/SOME_JOB/job/Adjusted-Performance-Test-Trigger/build'
BUILD_TOKEN = os.getenv('BUILD_TOKEN')
PARAMETERS = {'token': BUILD_TOKEN}
USER = os.getenv('USER')
API_TOKEN = os.getenv('API_TOKEN')

build_trigger_url = f'{SERVER_URL}/{JOB_BUILD}?{urlencode(PARAMETERS)}'

res = req.post(build_trigger_url, auth=(USER, API_TOKEN))
