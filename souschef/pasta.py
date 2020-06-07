{
    1: {
        "message": "Place a pan on the hob to start",
        1: {"func": _set_classifiers, "args": {"value": "pan_on_off,pasta,boilover"}},
        2: {"func": _set_hob_off},
        3: {"func": _classify, "args": {"model": "pan_on_off", "label": "pan_on"}},
    },
    2: {
        "message": "Add water to the pan",
        1: {"func": _classify, "args": {"model": "pasta", "label": "add_water"}},
    },
    3: {
        "message": "Autoheating water until boiling",
        1: {"func": _start_pan_detector},
        2: {"func": _set_fixed_setpoint, "args": {"value": 50}},
        3: {"func": _classify, "args": {"model": "pasta", "label": "water_boiling"}},
    },
    4: {
        "message": "Add 30g of pasta",
        1: {"func": _set_temperature_target, "args": {"value": 100}},
        2: {"func": _classify, "args": {"model": "pasta", "label": "add_pasta"}},
    },
    5: {
        "message": "Cooking for 15 minutes",
        1: {"func": _start_boilover_detector},
        2: {"func": _start_stir_detector, "args": {"duration": 180}},
        3: {"func": _start_timer, "args": {"name": "pasta", "duration": 12*60}},
        4: {"func": _poll_timer, "args": {"name": "pasta"}},
    },
    6: {"message": "12 minutes up. Pasta is cooked!", 
            1: {"func": _set_hob_off},
        },
}
