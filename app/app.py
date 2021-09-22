import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from sqlalchemy.sql import func
from flask import request
from sqlalchemy import and_

app = Flask(__name__)


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
    captured_time = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

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
        captured_time = datetime.datetime.now()
        add_sensor_value = SensorInfo(value=random_number, sensor_id=sensor_to_query,
                                      captured_time=captured_time)
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

    if sensor is None:
        return {'Message': "Sensor Id is not valid"}, 400

    if start_date_time and end_date_time:
        records = SensorInfo.query.filter(and_(SensorInfo.sensor_id == sensor_id, SensorInfo.captured_time >= start_date_time,
                                                SensorInfo.captured_time <= end_date_time))
        record_values = [(record.value, record.captured_time.strftime('%Y-%m-%d %H:%M:%S')) for record in records]
        return {'sensor_name': sensor.sensor_name,
                'number_of_values': len(record_values),
                'sensor_values': record_values}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
