{
    1: {
        "message": "Place a pan on the hob to start",
        1: {"func": _set_classifiers, "args": {"value": "pan_on_off,sauce,stirring"}},
        2: {"func": _set_hob_off},
        3: {"func": _classify, "args": {"model": "pan_on_off", "label": "pan_on"}},
    },
    2: {
        "message": "Add a tbsp of olive oil",
        1: {"func": _classify, "args": {"model": "sauce", "label": "add_oil"}},
    },
    3: {
        "message": "Autoheating until pan is hot",
        1: {"func": _start_pan_detector},
        2: {"func": _set_fixed_setpoint, "args": {"value": 20}},
        3: {"func": _set_temperature_target, "args": {"value": 100}},
        4: {"func": _poll_temperature, "args": {"target": 100}},
    },
    4: {
        "message": "Add 2 chopped onions",
        1: {"func": _classify, "args": {"model": "sauce", "label": "add_onions"}},
    },
    5: {
        "message": "Autocooking on a low heat until soft",
        1: {"func": _start_stir_detector, "args": {"duration": 60}},
        2: {"func": _classify, "args": {"model": "sauce", "label": "onions_cooked"}},
    },
    6: {
        "message": "Stir in 1 tbsp of tomato puree",
        1: {"func": _classify, "args": {"model": "sauce", "label": "add_puree"}},
    },
    7: {
        "message": "Autocooking for 2 minutes",
        1: {"func": _start_timer, "args": {"name": "puree", "duration": 3*60}},
        2: {"func": _poll_timer, "args": {"name": "puree"}},
    },
    8: {
        "message": "Add 2x400g cans of chopped tomatoes",
        1: {"func": _classify, "args": {"model": "sauce", "label": "add_puree"}},
    },
    9: {
        "message": "Autosimmering for 20 minutes",
        1: {"func": _start_timer, "args": {"name": "puree", "duration": 3*60}},
        2: {"func": _poll_timer, "args": {"name": "puree"}},
        3: {"func": _set_fixed_setpoint, "args": {"value": 20}},
        4: {"func": _set_temperature_target, "args": {"value": 90}},
    },
    10: {"message": "Sauce is cooked! Allow to cool for 10 minutes", 
            1: {"func": _set_hob_off},
        },
}
