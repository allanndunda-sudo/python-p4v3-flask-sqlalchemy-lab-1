# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


# @app.route('/')
# def index():
#     body = {'message': 'Flask SQLAlchemy Lab 1'}
#     return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        return make_response(
            jsonify({
                "id": earthquake.id,
                "magnitude": earthquake.magnitude,
                "location": earthquake.location,
                "year": earthquake.year
            }),
            200
        )
    else:
        return make_response(
            jsonify({
                "message": f"Earthquake {id} not found."
            }),
            404
        )


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    quakes_list = [
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        for quake in earthquakes
    ]

    return make_response(
        jsonify({
            "count": len(quakes_list),
            "quakes": quakes_list
        }),
        200
    )

# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)

