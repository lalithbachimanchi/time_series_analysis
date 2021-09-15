import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
import numpy as np
from sqlalchemy.sql import func
from flask import request


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lalith:Data_Mart123@localhost/data_analysis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


@app.route('/start_process/')
def update_sensor_values():
    iterations = request.args.get('iterations')
    create_sensor1 = Sensor(sensor_name='Sensor1')
    db.session.add(create_sensor1)
    db.session.commit()
      # create_sensor2 = Sensor(sensor_name='Sensor2')
    for _ in range(int(iterations)):
        random_number = np.random.random()
        captured_time = datetime.datetime.now()
        print(captured_time)
        add_sensor_value = SensorInfo(value=random_number, sensor_id=create_sensor1.sensor_id,
                                      captured_time=captured_time)
        db.session.add(add_sensor_value)
        db.session.commit()

    return {'Message':' Successfully Added Sensor Values',
            'number of records added': iterations}, 200


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


if __name__ == '__main__':
    app.run()