from flask import Flask
from flask import request
import control

ctrl = control.CONTROL()


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  # response.headers.add('Access-Control-Allow-Methods', 'GET,POST)
  return response

def index():
    if request.form['action'] == 'set_hob':
        return ctrl.set_hob(request.form['temp'])
    # return request.args.get('action')

if __name__ == '__main__':
    # TODO: add authentication
    app.run(debug=True, host='0.0.0.0')
