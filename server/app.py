# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        return jsonify({
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        })
    else:
        return jsonify({
            "message": f"Earthquake {id} not found."
        }), 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    quakes = [{
        'id': quake.id,
        'location': quake.location,
        'magnitude': quake.magnitude,
        'year': quake.year
    } for quake in earthquakes]
    
    return jsonify({
        'count': len(quakes),
        'quakes': quakes
    }), 200
