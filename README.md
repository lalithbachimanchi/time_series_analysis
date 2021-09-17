# time_series_analysis
How to run the application?

1. Install Docker
https://docs.docker.com/desktop/windows/install/

2. Go the repo folder in terminal

3. run the command docker-compose up

You will see log of installations happening....

In the log, you will find below stack trace
Serving Flask app 'app' (lazy loading)
app_1  |  * Environment: production
app_1  |    WARNING: This is a development server. Do not use it in a production deployment.
app_1  |    Use a production WSGI server instead.
app_1  |  * Debug mode: off
app_1  |  * Running on all addresses.
app_1  |    WARNING: This is a development server. Do not use it in a production deployment.
app_1  |  * Running on http://172.18.0.3:5000/ (Press CTRL+C to quit)

Copy the URL from stack trace

4. Hit in browser or postman http://172.18.0.3:5000/ 
  You should see a message "App is running"
  
5. API to add sensor values:
curl --location --request POST 'http://172.18.0.3:5000/post/insert_sensor_values?number_of_values=5&sensor_name=Sensor1'

6. API to receive Sensor Values:
curl --location --request GET 'http://172.18.0.3:5000/get/sensor_values/?sensor_id=1&start_date=2021-09-15 16:15:13&end_date=2021-09-17 22:11:13'
