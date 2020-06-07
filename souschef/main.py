from requests import post
from time import sleep, time
from threading import Thread
import logging

# Initialise custom logging format
FORMAT = "%(relativeCreated)6d %(levelname)-8s %(name)s %(process)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

ip = "http://" + "192.168.0.78" + ":5000/"


class SousChef(object):
    def __init__(self, recipe):
        self.latest_meta = {}
        self.timers = {}
        self.stop_flag = False
        self.previous_message = ""
        self.current_message = ""
        self.next_message = ""
        self.error_message = ""

        self.step_ID = 1
        self.substep_ID = 1

        # Import recipe from file
        with open(recipe, "r") as file:
            data = file.read().replace("\n", "")
        dispatch_table = eval(data)
        self.dispatch_table = dispatch_table

    def _post(self, data):
        try:
            r = post(ip, data)
            return r
        except:
            logger.info("Connection error")

    def _meta_worker(self):
        while True:
            data = {"action": "get_latest_meta"}
            r = self._post(data)
            try:
                self.latest_meta = dict(r.json())
            except AttributeError:
                pass
            sleep(0.1)

    def _worker(self):
        def _update_screen():
            step_ID = self.step_ID

            try:
                self.previous_message = self.dispatch_table[step_ID - 1]["message"]
            except KeyError:
                self.previous_message = "Onionbot is connected"

            try:
                self.current_message = self.dispatch_table[step_ID]["message"]
            except KeyError:
                print("hmmm")

            try:
                self.next_message = self.dispatch_table[step_ID + 1]["message"]
            except KeyError:
                self.next_message = "Recipe complete!"

        def _classify(args):

            model = args["model"]
            label = args["label"]
            logger.debug("Classifying Model %s | Label %s" % (model, label))

            meta = self.latest_meta
            try:
                data = meta["attributes"]["classification_data"]
                if data[model][label]["boolean"]:
                    logger.debug(
                        "Classifier: " + model + " " + label + " returned true"
                    )

                    # rolling_window = float(meta["attributes"]["interval"]) * 5
                    # logger.info("Sleeping for %s seconds..." % (rolling_window))
                    # sleep(rolling_window)
                    return True
            except KeyError:
                pass
            return False

        def _set_classifiers(args):
            value = args["value"]
            logger.debug("Setting classifiers")
            data = {"action": "set_classifiers", "value": str(value)}
            self._post(data)
            return True

        def _set_fixed_setpoint(args):
            value = args["value"]
            logger.debug("Setting fixed_setpoint")
            data = {"action": "set_fixed_setpoint", "value": str(value)}
            self._post(data)
            return True

        def _set_temperature_target(args):
            sleep(1)  # Time to allow initial fixed setpoint to send
            value = args["value"]
            logger.debug("Setting temperature_target")
            data = {"action": "set_temperature_target", "value": str(value)}
            self._post(data)
            return True

        def _set_hob_off():
            logger.debug("Turning hob off")
            data = {"action": "set_hob_off"}
            self._post(data)
            return True

        def _poll_temperature(args):
            target = args["target"]
            logger.debug("Turning hob off")
            try:
                temperature = self.latest_meta["attributes"]["temperature"]
            except KeyError:
                return False
            if float(temperature) > float(target):
                return True
            else:
                return False

        def _start_timer(args):
            name = args["name"]
            duration = float(args["duration"])
            self.timers[name] = time() + duration
            return True

        def _poll_timer(args):
            name = args["name"]
            if time() > self.timers[name]:
                return True
            else:
                return False

        # SPECIAL FUNCTIONS

        def _start_pan_detector():
            def _pan_worker():
                while True:
                    sleep(0.1)
                    try:
                        servo_setpoint = self.latest_meta["attributes"][
                            "servo_setpoint"
                        ]
                    except KeyError:
                        pass
                    else:
                        if _classify({"model": "pan_on_off", "label": "pan_off"}):
                            logger.info("No pan detected")
                            while True:
                                sleep(0.1)
                                if _classify(
                                    {"model": "pan_on_off", "label": "pan_off"}
                                ):
                                    _set_hob_off()
                                    self.error_message = "Return pan to hob to continue"
                                else:
                                    logger.info("Pan detected")
                                    self.error_message = ""
                                    _set_fixed_setpoint({"value": servo_setpoint})
                                    break

            Thread(target=_pan_worker, daemon=True).start()

        def _start_stir_detector(args):
            def _stir_worker():
                while True:
                    sleep(0.1)

                    if _classify({"model": "stirring", "label": "not_stirring"}):
                        while _poll_timer("stir_detector"):
                            sleep(0.1)
                            if _classify(
                                {"model": "stirring", "label": "not_stirring"}
                            ):
                                self.error_message = (
                                    "Pan has not been stirred for seconds "
                                    + duration
                                    + " seconds"
                                )
                            else:
                                logger.info("Stirring detected again")
                                self.error_message = ""
                                break
                    else:
                        _start_timer({"name": "stir_detector", "duration": duration})

            duration = args["duration"]
            Thread(target=_stir_worker, daemon=True).start()

        def _start_boilover_detector():
            def _boilover_worker():
                while True:
                    sleep(0.1)
                    try:
                        servo_setpoint = self.latest_meta["attributes"][
                            "servo_setpoint"
                        ]
                    except KeyError:
                        pass
                    else:
                        if _classify({"model": "boilover", "label": "boiling_over"}):
                            logger.info("Boilover event detected")
                            while True:
                                sleep(0.1)
                                if _classify(
                                    {"model": "boilover", "label": "boilover"}
                                ):
                                    _set_hob_off()
                                    self.error_message = "Pan is boiling over"
                                else:
                                    logger.info("Pan no longer boiling over")
                                    self.error_message = ""
                                    new_setpoint = float(servo_setpoint) * 0.9
                                    _set_fixed_setpoint({"value": new_setpoint})
                                    sleep(5)
                                    break

            Thread(target=_boilover_worker, daemon=True).start()

        # MAIN LOOP

        while True:
            result = False
            logger.info("Step %s | Substep %s" % (self.step_ID, self.substep_ID))

            while result is False and self.stop_flag is False:
                result = False
                step_ID = self.step_ID
                substep_ID = self.substep_ID
                substep = self.dispatch_table[step_ID][substep_ID]

                arguments = substep.get("args")
                if arguments:
                    result = substep["func"](args=arguments)
                else:
                    result = substep["func"]()

                _update_screen()

                sleep(0.1)

            # Increment all substeps then increment steps
            if self.stop_flag is True:
                break
            elif self.substep_ID + 1 in self.dispatch_table[self.step_ID].keys():
                self.substep_ID += 1
            elif self.step_ID + 1 in self.dispatch_table.keys():
                self.step_ID += 1
                self.substep_ID = 1
            else:
                break  # Recipe is complete

    def next(self):
        if self.step_ID + 1 in self.dispatch_table.keys():
            logger.info("Next called")
            self.substep_ID = 1
            self.step_ID += 1

    def previous(self):
        if self.step_ID - 1 in self.dispatch_table.keys():
            logger.info("Previous called")
            self.substep_ID = 1
            self.step_ID -= 1

    def run(self):
        Thread(target=self._meta_worker, daemon=True).start()
        Thread(target=self._worker, daemon=True).start()
