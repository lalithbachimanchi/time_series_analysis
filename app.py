
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from sqlalchemy.sql import func
from flask import request
from sqlalchemy.sql import text
from sqlalchemy import and_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lalith:Data_Mart123@localhost/data_analysis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


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


@app.route('/get/sensor_values/')
def get_sensor_values():
    sensor_id = request.args.get('sensor_id')
    start_date_time = request.args.get('start_date')
    end_date_time = request.args.get('end_date')

    sensor_name = Sensor.query.filter_by(sensor_id=sensor_id).first().sensor_name

    if start_date_time and end_date_time:
        records = SensorInfo.query.filter(and_(text(sensor_id), SensorInfo.captured_time >= start_date_time,
                                     SensorInfo.captured_time <= end_date_time))
        record_values = [record.value for record in records]
        return {'sensor_name': sensor_name,
                'number_of_values': len(record_values),
                'sensor_values': record_values}, 200

if __name__ == '__main__':

   app.run(debug=True,port=9234)
   # app.run()
   # st_p()
