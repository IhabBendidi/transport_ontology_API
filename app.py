import flask
import rdflib


app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = "data"
app.config["DEBUG"] = True


@app.route('/api/moyen_transports', methods=['GET'])
def enroll():
    pass
