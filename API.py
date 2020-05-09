from flask import Flask
from flask import request

from flask_cors import CORS

from main import OnionBot

import os
import sys

import logging

logger = logging.getLogger("werkzeug")
logger.setLevel(logging.ERROR)


logger.info("Initialising web server")
app = Flask(__name__)
CORS(app)

bot = OnionBot()

logger.info("Web server ready. Go to 0.0.0.0:8888/portal to connect")

bot.run()


@app.route("/", methods=["GET", "POST"])
def index():
    """Index is run automatically on init by flask"""

    if request.form["action"] == "start":
        logger.debug("start called")
        return bot.start(request.form["value"])

    if request.form["action"] == "stop":
        logger.debug("stop called")
        return bot.stop()

    if request.form["action"] == "get_latest_meta":
        logger.debug("get_latest_meta called")
        return bot.get_latest_meta()

    if request.form["action"] == "get_thermal_history":
        logger.debug("get_thermal_history called")
        return bot.get_thermal_history()

    if request.form["action"] == "get_chosen_labels":
        logger.debug("get_chosen_labels called")
        return bot.get_chosen_labels()

    if request.form["action"] == "set_chosen_labels":
        logger.debug("set_chosen_labels called")
        return bot.set_chosen_labels(request.form["value"])

    if request.form["action"] == "set_active_label":
        logger.debug("set_active_label called")
        return bot.set_active_label(request.form["value"])

    if request.form["action"] == "set_active_model":
        logger.debug("set_active_model called")
        return bot.set_active_model(request.form["value"])

    if request.form["action"] == "get_temperature_setpoint":
        logger.debug("get_temperature_setpoint called")
        return bot.get_temperature_setpoint()

    if request.form["action"] == "get_camera_frame_rate":
        logger.debug("get_camera_frame_rate called")
        return bot.get_camera_frame_rate()

    if request.form["action"] == "set_fixed_setpoint":
        logger.debug("set_fixed_setpoint called")
        return bot.set_fixed_setpoint(request.form["value"])

    if request.form["action"] == "set_temperature_target":
        logger.debug("set_temperature_target called")
        return bot.set_temperature_target(request.form["value"])

    if request.form["action"] == "set_temperature_hold":
        logger.debug("set_temperature_hold called")
        return bot.set_temperature_hold()

    if request.form["action"] == "set_hob_off":
        logger.debug("set_hob_off called")
        return bot.set_hob_off()

    if request.form["action"] == "set_pid_enabled":
        logger.debug("set_pid_enabled called")
        return bot.set_pid_enabled(request.form["value"])

    if request.form["action"] == "set_p_coefficient":
        logger.debug("set_p_coefficient called")
        return bot.set_p_coefficient(request.form["value"])

    if request.form["action"] == "set_i_coefficient":
        logger.debug("set_i_coefficient called")
        return bot.set_i_coefficient(request.form["value"])

    if request.form["action"] == "set_d_coefficient":
        logger.debug("set_d_coefficient called")
        return bot.set_d_coefficient(request.form["value"])

    if request.form["action"] == "set_pid_reset":
        logger.debug("set_pid_reset called")
        return bot.set_pid_reset()

    if request.form["action"] == "set_frame_interval":
        logger.debug("set_frame_interval called")
        return bot.set_frame_interval(request.form["value"])

    if request.form["action"] == "get_all_labels":
        logger.debug("get_all_labels called")
        return bot.get_all_labels()

    if request.form["action"] == "get_all_models":
        logger.debug("get_all_models called")
        return bot.get_all_models()

    if request.form["action"] == "quit":
        logger.debug("quit called")
        bot.quit()
        logger.info("Shutting down server")
        server_quit = request.environ.get("werkzeug.server.shutdown")
        if server_quit is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        server_quit()
        sys.exit()
        os.system("sleep 1 ; pkill -f API.py")  # If all else fails...


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
