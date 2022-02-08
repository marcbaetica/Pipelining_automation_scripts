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


if any([item is None for item in PARAMETERS.values()]):
    raise ValueError(f'Some of the build trigger parameters were not found (alue is None).'
                     f' Check your .env definitions. Received: {PARAMETERS}')

if USER is None or API_TOKEN is None:
    raise ValueError(f'Either the username or api token were not found (value is None). Check your .env definitions.')


build_trigger_url = f'{SERVER_URL}/{JOB_BUILD}?{urlencode(PARAMETERS)}'

res = req.post(build_trigger_url, auth=(USER, API_TOKEN))
res.raise_for_status()
