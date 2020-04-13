from main import OnionBot


from flask import Flask
from flask import request

from flask_cors import CORS

import logging

bot = OnionBot()

logging.info("Initialising web server")
app = Flask(__name__)
CORS(app)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


logging.info("Web server ready. Go to 0.0.0.0:8888/portal to connect")


@app.route("/", methods=["GET", "POST"])
def index():
    """Index is run automatically on init by flask"""

    if request.form["action"] == "start":
        return bot.start(request.form["value"])

    if request.form["action"] == "stop":
        return bot.stop()

    if request.form["action"] == "get_latest_meta":
        return bot.get_latest_meta()

    if request.form["action"] == "get_temperature_window":
        return bot.get_temperature_window()

    if request.form["action"] == "get_chosen_labels":
        return bot.get_chosen_labels()

    if request.form["action"] == "set_chosen_labels":
        return bot.set_chosen_labels(request.form["value"])

    if request.form["action"] == "set_active_label":
        return bot.set_active_label(request.form["value"])

    if request.form["action"] == "set_active_model":
        return bot.set_active_model(request.form["value"])

    if request.form["action"] == "get_temperature_setpoint":
        return bot.get_temperature_setpoint()

    if request.form["action"] == "get_camera_frame_rate":
        return bot.get_camera_frame_rate()

    if request.form["action"] == "set_hob_setpoint":
        return bot.set_hob_setpoint(request.form["value"])

    if request.form["action"] == "set_hob_off":
        return bot.set_hob_off()

    if request.form["action"] == "set_camera_sleep":
        return bot.set_camera_sleep(request.form["value"])

    if request.form["action"] == "get_all_labels":
        return bot.get_all_labels()

    if request.form["action"] == "get_all_models":
        return bot.get_all_models()


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
