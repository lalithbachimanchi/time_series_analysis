import datetime
from time import sleep
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_ngrok import run_with_ngrok
import numpy as np
from sqlalchemy.sql import func
from flask import request
from sqlalchemy.dialects.mysql import DATETIME
import mysql.connector

app = Flask(__name__)
# run_with_ngrok(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db/data_analysis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['debug'] = True
db = SQLAlchemy(app)


class Sensor(db.Model):
    __tablename__ = 'sensor'
    sensor_id = db.Column(db.Integer, primary_key=True)
    sensor_name = db.Column(db.String(120), nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class SensorInfo(db.Model):
    __tablename__ = 'sensor_info'
    sensor_info_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.ForeignKey('sensor.sensor_id'), nullable=False, index=True)
    value = db.Column(db.Float, nullable=False)
    created_time = db.Column(DATETIME(fsp=6))

@app.route('/')
def index():
    return 'App is Running'


@app.route('/post/insert_sensor_values/', methods=['POST'])
def insert_sensor_values():
    sensor_name = str(request.args.get('sensor_name'))

    try:
        num_value = int(request.args.get('number_of_values'))
    except:
        return {'Message': 'number_of_values must be an Integer'}, 400

    check_sensor = Sensor.query.filter_by(sensor_name=sensor_name).first()

    sensor_to_query = None
    if not check_sensor:
        create_sensor = Sensor(sensor_name=sensor_name)
        db.session.add(create_sensor)
        db.session.commit()
        sensor_to_query = create_sensor.sensor_id
    else:
        sensor_to_query = check_sensor.sensor_id
    for _ in range(int(num_value)):
        random_number = np.random.random()
        add_sensor_value = SensorInfo(value=random_number, sensor_id=sensor_to_query)
        db.session.add(add_sensor_value)
    db.session.commit()

    return {'Message': 'Successfully Added Sensor Values',
            'sensor_id': sensor_to_query,
            'number of records added': num_value}, 200


@app.route('/get/sensor_values/')
def get_sensor_values():
    start_date_time = request.args.get('start_date')
    end_date_time = request.args.get('end_date')

    try:
        sensor_id = int(request.args.get('sensor_id'))
    except:
        return {'Message': 'sensor_id must be an Integer'}, 400

    try:
        datetime.datetime.strptime(start_date_time, '%Y-%m-%d %H:%M:%S')
        datetime.datetime.strptime(end_date_time, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        return {"Message": "Incorrect datetime format, should be YYYY-MM-DD HH:MM:SS"}, 400

    sensor = Sensor.query.filter_by(sensor_id=sensor_id).first()

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'data_analysis'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT value, created_time FROM sensor_info where sensor_id={} and created_time >= "{}" and created_time <= "{}"'.format(sensor_id, start_date_time, end_date_time))
    results = [(value, created_time.strftime('%Y-%m-%d %H:%M:%S.%f')) for (value, created_time) in cursor]
    cursor.close()
    connection.close()

    if sensor is None:
        return {'Message': "Sensor Id is not valid"}, 400
    return {'sensor_name': sensor.sensor_name,
            'number_of_values': len(results),
            'sensor_values': results}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
