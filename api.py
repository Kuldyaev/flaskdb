from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://slava:Vlada2004@localhost/slava'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

   
class Measurement(db.Model):
  __tablename__ = 'measurements'
  m_id = db.Column(db.Integer, primary_key=True)
  m_object = db.Column(db.String(), nullable=False) 
  m_operator = db.Column(db.String(), nullable=False)
  m_requestDateTime = db.Column(db.DateTime, nullable=False)
  m_date = db.Column(db.Date, nullable=False)
  m_time = db.Column(db.Time, nullable=False)
  m_temp = db.Column(db.Integer, nullable=False)
  m_pres = db.Column(db.Integer, nullable=False) 
  m_air_hum = db.Column(db.Integer, nullable=False)
  m_soil_hum = db.Column(db.Integer, nullable=False)
  m_comments = db.Column(db.String(), nullable=False)
 
  
db.create_all()


@app.route('/')
def index():
  lastmeas = Measurement.query.first()
  return    "Последние данные: " + lastmeas.m_operator + " cooбщил, что " + lastmeas.m_object + " на "+ lastmeas.m_time.__str__() + " " + lastmeas.m_date.__str__() + " имеет параметры  температура-" + lastmeas.m_temp.__str__() +"С  давление воздуха-" + lastmeas.m_pres.__str__()

@app.route('/measurements', methods=['POST', 'GET'])
def handle_measurements():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_measurement = Measurement(m_object=data['object'], m_date=data['date'], m_time=data['time'], 
								m_temp=data['temp'], m_pres=data['pres'], m_air_hum=data['air_hum'], m_soil_hum=data['soil_hum'],
								m_comments=data['comments'], m_operator=data['operator'], m_requestDateTime=datetime.now())
            db.session.add(new_measurement)
            db.session.commit()
            return {"message": f"measurement {new_measurement.m_object} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        measurements = Measurement.query.all()
        results = [
            {
				"operator": measurement.m_operator,	
                "object": measurement.m_object,
                "date": measurement.m_date,
                "time": measurement.m_time.__str__(),
				"temp": measurement.m_temp,
                "air_hum": measurement.m_air_hum,
				"soil_hum": measurement.m_soil_hum,
                "pres": measurement.m_pres,
				"comments": measurement.m_comments
            } for measurement in measurements]

        return {"count": len(measurements), "measurements": results}  
	
	

if __name__=='__main__':
	app.run(debug=True)
