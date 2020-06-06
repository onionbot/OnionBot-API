{
    1: {
        "message": "Place a pan on the hob to start",
        1: {
            "func": _set_classifiers,
            "args": {
                "value": "pan_on_off,pasta"
            }
        },
        2: {
            "func": _set_hob_off
        },
        3: {
            "func": _classify,
            "args": {
                "model": "pan_on_off",
                "label": "pan_on"
            }
        },
        4: {
            "func": _classify,
            "args": {
                "model": "pasta",
                "label": "empty_pan"
            }
        },
    },
    2: {
        "message": "Add 300ml of water",
        1: {
            "func": _classify,
            "args": {
                "model": "pasta",
                "label": "add_water"
            }
        }
    },
    3: {
        "message": "Autoheating water until boiling",
        1: {
            "func": _set_fixed_setpoint,
            "args": {
                "value": 50
            }
        },
        2: {
            "func": _classify,
            "args": {
                "model": "pasta",
                "label": "water_boiling"
            }
        },

    },
    4: {
        "message": "Add 30g of pasta",
        1: {
            "func": _classify,
            "args": {
                "model": "pasta",
                "label": "add_pasta"
            }
        },

    },
    5: {
        "message": "Cooking for 10 seconds",
        1: {
            "func": _start_timer,
            "args": {
                "name": "pasta",
                "duration": 10
            }
        },
        2: {
            "func": _poll_timer,
            "args": {
                "name": "pasta"
            }
        },
    },
    6: {
        "message": "Pasta is ready",
        1: {
            "func": _set_hob_off
        },
}