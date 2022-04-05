#!flask/bin/python3
import string
import os
import random
import flask
from werkzeug import utils as wz_utils
from prometheus_flask_exporter import PrometheusMetrics

from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from . import alphabot_exceptions
from . import dna


DEFAULT_IP_ADDR = '0.0.0.0'
DEFAULT_PORT = 8000

IP_ADDR = os.getenv('EDGE_SERVER_IP_ADDR')
if IP_ADDR is None:
    print("Environmemnt variable 'EDGE_SERVER_IP_ADDR' is not set, using "
          "default ip: %s" % DEFAULT_IP_ADDR)
    IP_ADDR = DEFAULT_IP_ADDR

PORT = os.getenv('EDGE_SERVER_PORT')
if PORT is None:
    print("Environmemnt variable 'EDGE_SERVER_PORT' is not set, using "
          "default port: %d" % DEFAULT_PORT)
    PORT = DEFAULT_PORT
else:
    PORT = int(PORT)

D = dna.Dna()
app = flask.Flask(__name__)
metrics = GunicornPrometheusMetrics(app)
metrics = PrometheusMetrics(app)

@app.route('/', methods=['GET', 'POST'])
def post_image():
    if flask.request.method != 'POST':
        return "%s \n" % flask.request.method

    file = flask.request.files['file']
    filename = wz_utils.secure_filename(file.filename)
    random_string = ''.join(
        random.choice(string.ascii_uppercase +
                      string.digits) for _ in range(15))
    final_image_name = '{}_{}'.format(filename, random_string)
    file.save(final_image_name)
    dirr = os.getcwd()
    osname = os.path.join(dirr, '')
    dest_img = osname + final_image_name
    try:
        results = D.find_distance_and_angle(dest_img)  ### pairnei path
        os.remove(dest_img)
        return flask.jsonify(results)
    except alphabot_exceptions.BeaconNotFoundError:
        os.remove(dest_img)
        return flask.abort(404)

def main():
    app.run(host=IP_ADDR, port=PORT)#, threaded=True)

if __name__ == '__main__':
    main()
