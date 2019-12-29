from flask import Flask
from flask import request
import control 

ctrl = control.CONTROL()


app = Flask(__name__)

@app.route('/')
def index():
    if request.args.get('action') == 'set_hob':
        return ctrl.set_hob(request.args.get('temp')) 
    # return request.args.get('action')

if __name__ == '__main__':
    # TODO: add authentication 
    app.run(debug=True, host='0.0.0.0')

