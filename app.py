
from API import ONIONAPI
api = ONIONAPI()

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
    #     return api.set_hob(request.form['temp'])
    # # return request.args.get('action')

    if request.form['action'] == 'start':
        return api.start(request.form['value'])


    if request.form['action'] == 'stop':
        return api.stop()


    if request.form['action'] == 'get_latest_meta':
        return api.get_latest_meta()


    if request.form['action'] == 'get_chosen_labels':
        return api.get_chosen_labels()


    if request.form['action'] == 'set_chosen_labels':
        return api.set_chosen_labels(request.form['value'])


    if request.form['action'] == 'set_active_label':
        return api.set_active_label(request.form['value'])


    if request.form['action'] == 'set_active_model':
        return api.set_active_model(request.form['value'])


    if request.form['action'] == 'get_temperature_setpoint':
        return api.get_temperature_setpoint()


    if request.form['action'] == 'get_camera_frame_rate':
        return api.get_camera_frame_rate()


    if request.form['action'] == 'set_hob_setpoint':
        return api.set_hob_setpoint(request.form['value'])


    if request.form['action'] == 'set_camera_sleep':
        return api.set_camera_sleep(request.form['value'])


    if request.form['action'] == 'get_all_labels':
        return api.get_all_labels()


    if request.form['action'] == 'get_all_models':
        return api.get_all_models()

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
    

