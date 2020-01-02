
from local import LOCAL
local = LOCAL()

from flask import Flask
from flask import request
from flask import send_file

from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET','POST'])
def index():
    """Index is run automatically on init by flask"""
    
    # if request.form['action'] == 'set_hob':
    #     return local.set_hob(request.form['temp'])
    # # return request.args.get('action')

    if request.form['action'] == 'start':
        return local.start(request.form['value'])


    if request.form['action'] == 'stop':
        return local.stop()


    if request.form['action'] == 'get_latest_meta':
        return local.get_latest_meta()


    if request.form['action'] == 'get_chosen_labels':
        return local.get_chosen_labels()


    if request.form['action'] == 'set_chosen_labels':
        return local.set_chosen_labels(request.form['value'])


    if request.form['action'] == 'set_active_label':
        return local.set_active_label(request.form['value'])


    if request.form['action'] == 'set_active_model':
        return local.set_active_model(request.form['value'])


    if request.form['action'] == 'get_temperature_setpoint':
        return local.get_temperature_setpoint()


    if request.form['action'] == 'get_camera_frame_rate':
        return local.get_camera_frame_rate()


    if request.form['action'] == 'set_hob_setpoint':
        return local.set_hob_setpoint(request.form['value'])


    if request.form['action'] == 'set_camera_sleep':
        return local.set_camera_sleep(request.form['value'])


    if request.form['action'] == 'get_all_labels':
        return local.get_all_labels()


    if request.form['action'] == 'get_all_models':
        return local.get_all_models()

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
    

