from flask import Flask
from flask import request
from flask_cors import CORS

from souschef import SousChef

import logging

# Silence Flask werkzeug logger
logger = logging.getLogger("werkzeug")
logger.setLevel(logging.ERROR)  # Note! Set again below

# Initialise SousChef
sous = SousChef()

# Initialise flask server
app = Flask(__name__)
CORS(app)

sous.run()


@app.route("/", methods=["GET", "POST"])
def index():
    """Index is run automatically on init by flask"""

    if request.form["action"] == "get_screen_message":
        logger.debug("get_message called")
        return sous.screen_message

    if request.form["action"] == "next":
        logger.debug("next called")
        sous.next()
        return "1"

    if request.form["action"] == "previous":
        logger.debug("previous called")
        sous.previous()
        return "1"

    if request.form["action"] == "stop":
        logger.debug("stop called")
        sous.stop()
        return "1"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="5001")
