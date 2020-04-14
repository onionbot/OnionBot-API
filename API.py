
from flask import Flask
from flask import request

from flask_cors import CORS

from main import OnionBot

import logging

FORMAT = "%(relativeCreated)6d %(levelname)-8s %(module)s %(process)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


# log = logging.getLogger("werkzeug")
# log.setLevel(logging.ERROR)


logging.info("Initialising web server")
app = Flask(__name__)
CORS(app)

bot = OnionBot()

logging.info("Web server ready. Go to 0.0.0.0:8888/portal to connect")

bot.run()


@app.route("/", methods=["GET", "POST"])
def index():
    """Index is run automatically on init by flask"""

    if request.form["action"] == "start":
        return bot.start(request.form["value"])

    if request.form["action"] == "stop":
        return bot.stop()

    if request.form["action"] == "quit":
        return bot.quit()

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
