import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

data = requests.get('http://172.18.0.3:5000/get/sensor_values/?sensor_id=1&start_date=2021-09-15 16:15:13&end_date=2021-10-25 22:11:13').json()

# with open('/home/lalith/Documents/large_resp_microseconds.json') as json_file:
#     data = json.load(json_file)


# df = pd.read_json('/home/lalith/Documents/just5.json')
df2 = pd.DataFrame(data=data['sensor_values'], columns=['value','date'])

# df2['date'] = pd.to_datetime(df2['date'])



# create the time series plot
sns.lineplot(x="Date", y="Col_1",
             data=df2)

plt.xticks(rotation=25)