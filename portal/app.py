from flask import Flask
from flask import request

from server import SERVER

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

server = SERVER()


@app.route('/', methods=['GET','POST'])


def index():
	"""Index is run automatically on init by flask"""
    
    # if request.form['action'] == 'set_hob':
    #     return server.set_hob(request.form['temp'])
    # # return request.args.get('action')


    if request.form['action'] == 'start':
        return server.start(request.form['value']):


    if request.form['action'] == 'stop':
        return server.stop():


    if request.form['action'] == 'get_latest_meta':
        return server.get_latest_meta():


    if request.form['action'] == 'get_chosen_labels':
        return server.get_chosen_labels():


    if request.form['action'] == 'set_chosen_labels':
        return server.set_chosen_labels(request.form['value']):


    if request.form['action'] == 'set_active_label':
        return server.set_active_label(request.form['value']):


    if request.form['action'] == 'set_active_model':
        return server.set_active_model(request.form['value']):


    if request.form['action'] == 'get_temperature_setpoint':
        return server.get_temperature_setpoint():


    if request.form['action'] == 'get_camera_frame_rate':
        return server.get_camera_frame_rate():


    if request.form['action'] == 'set_temperature_setpoint':
        return server.set_temperature_setpoint(float(request.form['value'])):


    if request.form['action'] == 'set_camera_frame_rate':
        return server.set_camera_frame_rate(float(request.form['value'])):


    if request.form['action'] == 'get_all_labels':
        return server.get_all_labels():


    if request.form['action'] == 'get_all_models':
        return server.get_all_models():



if __name__ == '__main__':
    # TODO: add authentication
    app.run(debug=True, host='0.0.0.0')
