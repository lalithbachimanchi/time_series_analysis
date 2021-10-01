import numpy as np
import pandas as pd

import requests

data = requests.get('http://172.18.0.3:5000/get/sensor_values/?sensor_id=2&start_date=2021-09-15 16:15:13&end_date=2021-09-25 22:11:13').json()

df = pd.read_json('/home/lalith/Documents/just5.json')

# df2 = pd.DataFrame(data=data['sensor_values'])
df2 = pd.DataFrame(data=data['sensor_values'],columns=['value','date'])

import pdb
pdb.set_trace()