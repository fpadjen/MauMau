import os
from flask import Flask, send_from_directory
from flask.ext import restful  # @UnresolvedImport

app = Flask(__name__, template_folder='../templates', static_folder='../static')
api = restful.Api(app)


@app.route('/bower_components/<path:filename>')
def bower_components(filename):
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bower_components')), filename)


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=True)
    app.debug = True
