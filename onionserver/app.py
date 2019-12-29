from flask import Flask
from flask import request

import control

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

ctrl = control.CONTROL()


@app.route('/', methods=['GET','POST'])


def index():
    if request.form['action'] == 'set_hob':
        return ctrl.set_hob(request.form['temp'])
    # return request.args.get('action')

if __name__ == '__main__':
    # TODO: add authentication
    app.run(debug=True, host='0.0.0.0')
