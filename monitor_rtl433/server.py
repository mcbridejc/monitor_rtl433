import flask
import json
from flask_table import Table, Col
import pprint

# Declare your table
class SensorTable(Table):
    model = Col('Model')
    id = Col('SensorId')
    time = Col('Timestamp')
    json = Col('JSON data')

def raw_sensor_string(sensor):
    s = ""
    for k,v in sensor.items():
        s += "%s=%s<br/>" % (k, str(v))
    return s

def create_app(sensor_db, metric_maker):
    app = flask.Flask(__name__)
    @app.route("/")
    def index():
        return flask.render_template('index.html')

    @app.route("/metrics")
    def metrics():
        return flask.Response(metric_maker.to_string(sensor_db.recent()), mimetype='text/plain')

    @app.route ("/sensors.json")
    def sensors_json():
        return flask.Response(json.dumps(sensor_db.all()), mimetype='application/json')

    @app.route("/sensors")
    def sensors():
        items = [
            {
                'model': s['model'],
                'id': s.get('id', 'N/A'),
                'time': s['time'],
                'json': flask.Markup(raw_sensor_string(s)),
            } 
            for s in sensor_db.all()
        ]
        items = sorted(items, key=lambda x: x['time'], reverse=True)
        table = SensorTable(items)
        return flask.render_template('sensors.html', sensor_table=table)
    return app