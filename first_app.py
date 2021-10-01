import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import requests
import json
import altair as alt
import time


st.title('My first app')


# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))

# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])
#
# st.line_chart(chart_data)
#
#
# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])
#
# st.map(map_data)

# df = pd.DataFrame({
#   'date': ['10/1/2019','10/2/2019', '10/3/2019', '10/4/2019'],
#   'values': [10, 20, 30, 40]
# })

data = requests.get('http://172.18.0.3:5000/get/sensor_values/?sensor_id=6&start_date=2021-09-15 16:15:13&end_date=2021-10-25 22:11:13').json()

# with open('/home/lalith/Documents/large_resp_microseconds.json') as json_file:
#     data = json.load(json_file)


# df = pd.read_json('/home/lalith/Documents/just5.json')
df2 = pd.DataFrame(data=data['sensor_values'], columns=['value','date'])

df2['date'] = pd.to_datetime(df2['date'])

lines = alt.Chart(df2).mark_line().encode(
  x=alt.X('1:T',axis=alt.Axis(title='date')),
  y=alt.Y('0:Q',axis=alt.Axis(title='value'))
  ).properties(
      width=600,
      height=300
  )

# Plot a Chart
def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
    x=alt.X('date:T', axis=alt.Axis(title='date')),
    y=alt.Y('value:Q',axis=alt.Axis(title='value')),
    ).properties(
        width=600,
        height=300
    )
    return lines


N = df2.shape[0] # number of elements in the dataframe
burst = 6       # number of elements (months) to add to the plot
size = burst    # size of the current dataset

# Plot Animation
line_plot = st.altair_chart(lines)
start_btn = st.button('Start')

if start_btn:
    for i in range(1,N):
        step_df = df2.iloc[0:size]
        lines = plot_animation(step_df)
        line_plot = line_plot.altair_chart(lines)
        size = i + burst
        if size >= N:
            size = N - 1
        time.sleep(0.1)




# df2 = df2.rename(columns={'date':'index'}).set_index('index')

# df2

# st.line_chart(df2)