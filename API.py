from flask import Flask
from flask import request

from flask_cors import CORS

from main import OnionBot

import os
import sys

import logging


# # Fix logging faliure issue
# for handler in logging.root.handlers[:]:
#     logging.root.removeHandler(handler)

FORMAT = "%(relativeCreated)6d %(levelname)-8s %(name)s %(process)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger("API")

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.ERROR)


logger.info("Initialising web server...")
app = Flask(__name__)
CORS(app)

bot = OnionBot()
logger.info("OnionBot is ready")

logger.info("Web server is ready. Go to 0.0.0.0:8888/portal to connect")

logger.info("Starting main script")
bot.run()


@app.route("/", methods=["GET", "POST"])
def index():
    """Index is run automatically on init by flask"""

    if request.form["action"] == "start":
        logger.debug("start called")
        bot.start(request.form["value"])
        return "1"

    if request.form["action"] == "stop":
        logger.debug("stop called")
        return bot.stop()

    if request.form["action"] == "get_latest_meta":
        logger.debug("get_latest_meta called")
        return bot.get_latest_meta()

    if request.form["action"] == "get_thermal_history":
        logger.debug("get_thermal_history called")
        return bot.get_thermal_history()

    if request.form["action"] == "set_label":
        logger.debug("set_label called")
        bot.set_label(request.form["value"])
        return "1"

    if request.form["action"] == "set_no_label":
        logger.debug("set_no_label called")
        bot.set_no_label()
        return "1"

    if request.form["action"] == "set_active_model":
        logger.debug("set_active_model called")
        bot.set_active_model(request.form["value"])
        return "1"

    if request.form["action"] == "get_temperature_setpoint":
        logger.debug("get_temperature_setpoint called")
        return bot.get_temperature_setpoint()

    if request.form["action"] == "get_camera_frame_rate":
        logger.debug("get_camera_frame_rate called")
        return bot.get_camera_frame_rate()

    if request.form["action"] == "set_fixed_setpoint":
        logger.debug("set_fixed_setpoint called")
        bot.set_fixed_setpoint(request.form["value"])
        return "1"

    if request.form["action"] == "set_temperature_target":
        logger.debug("set_temperature_target called")
        bot.set_temperature_target(request.form["value"])
        return "1"

    if request.form["action"] == "set_temperature_hold":
        logger.debug("set_temperature_hold called")
        bot.set_temperature_hold()
        return "1"

    if request.form["action"] == "set_hob_off":
        logger.debug("set_hob_off called")
        bot.set_hob_off()
        return "1"

    if request.form["action"] == "set_pid_enabled":
        logger.debug("set_pid_enabled called")
        bot.set_pid_enabled(request.form["value"])
        return "1"

    if request.form["action"] == "set_p_coefficient":
        logger.debug("set_p_coefficient called")
        bot.set_p_coefficient(request.form["value"])
        return "1"

    if request.form["action"] == "set_i_coefficient":
        logger.debug("set_i_coefficient called")
        bot.set_i_coefficient(request.form["value"])
        return "1"

    if request.form["action"] == "set_d_coefficient":
        logger.debug("set_d_coefficient called")
        bot.set_d_coefficient(request.form["value"])
        return "1"

    if request.form["action"] == "set_pid_reset":
        logger.debug("set_pid_reset called")
        bot.set_pid_reset()
        return "1"

    if request.form["action"] == "set_frame_interval":
        logger.debug("set_frame_interval called")
        bot.set_frame_interval(request.form["value"])
        return "1"

    if request.form["action"] == "get_all_labels":
        logger.debug("get_all_labels called")
        return bot.get_all_labels()

    if request.form["action"] == "get_all_models":
        logger.debug("get_all_models called")
        return bot.get_all_models()

    if request.form["action"] == "pi-restart":
        os.system("sudo reboot")

    if request.form["action"] == "pi-shutdown":
        os.system("sudo shutdown now")

    if request.form["action"] == "restart":
        os.system(". ~/onionbot/runonion")

    if request.form["action"] == "quit":
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
