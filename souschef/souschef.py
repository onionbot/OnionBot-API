from flask import Flask
from flask import request
from flask_cors import CORS

from main import SousChef
import sys

import logging

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("recipe")
args = parser.parse_args()

# Silence Flask werkzeug logger
logger = logging.getLogger("werkzeug")
logger.setLevel(logging.ERROR)  # Note! Set again below


# Silence Flask werkzeug logger
logger = logging.getLogger("werkzeug")
logger.setLevel(logging.ERROR)  # Note! Set again below

# Initialise SousChef
sous = SousChef(args.recipe)

# Initialise flask server
app = Flask(__name__)
CORS(app)

sous.run()


@app.route("/", methods=["GET", "POST"])
def index():
    """Index is run automatically on init by flask"""

    if request.form["action"] == "current_message":
        logger.debug("current_message called")
        return str(sous.current_message)

    if request.form["action"] == "previous_message":
        logger.debug("previous_message called")
        return str(sous.previous_message)

    if request.form["action"] == "next_message":
        logger.debug("next_message called")
        return str(sous.next_message)

    if request.form["action"] == "error_message":
        logger.debug("error_message called")
        return str(sous.error_message)

    if request.form["action"] == "next":
        logger.debug("next called")
        sous.next()
        return "1"

    if request.form["action"] == "previous":
        logger.debug("previous called")
        sous.previous()
        return "1"

    if request.form["action"] == "stop":
        server_quit = request.environ.get("werkzeug.server.shutdown")
        if server_quit is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        server_quit()
        sys.exit()


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="5001")
