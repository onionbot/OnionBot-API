// -------------------------------------------------------
// PORTAL.JS COPYRIGHT BEN COBLEY 2020 




// -------------------------------------------------------
// ---------------- APPLICATION VARIABLES ----------------

if (!localStorage.ip_address) {
    localStorage.ip_address = "192.168.0.1";
}

var endpoint_url = 'http://' + localStorage.ip_address + ':5000/';
var update_interval = 100;
var connected = false;
var previous_meta = null;
// var ctx = document.getElementById('myChart').getContext('2d');

var $table = $('#table');
var mydata =
    [{
            "label": "not_boiling",
            "count": 5
        }, {
            "label": "boiling",
            "count": 6
        }, {
            "label": "test2",
            "count": 6
        },

    ];

function badgeFormatter(value) {
    return '<span class="badge badge-light" style="font-size: 18px;">' + value + '</span>'
}

$(function() {
    $('#table').bootstrapTable({
        data: mydata
    });
});

// ------------------ INTERFACE WITH API ----------------

function set(function_name, argument) {
    $.ajax({
        type: 'POST',
        url: endpoint_url,
        data: {
            action: function_name,
            value: argument
        },
        success: function(confirmation) {},
    });
}


function get(function_name, callback) {
    $.ajax({
        type: 'POST',
        url: endpoint_url,
        data: {
            action: function_name,
        },
        success: callback,
        error: connection_failed,
    });

}


// ------------- UPDATE FREQUENTLY -------------

function update() {

    get("get_latest_meta", function(data) {
        // data is a js object 

        connection_success()

        // Only refresh when new data
        if (data == previous_meta) {
            // Update previous meta
            previous_meta = data
        }

        else {
            // Update previous meta
            previous_meta = data

            console.log("Refreshing")

            // console.log(data)

            // console.log(previous_meta)

            meta = JSON.parse(data);

            // Update key information
            $('#session-id-output').html(meta.attributes.session_name);
            $('#active-label').html(meta.attributes.active_label);
            $('#measurement-id').html(meta.attributes.measurement_id);
            $('#time-stamp').html(meta.attributes.time_stamp);


            // Update live data


            // Load new images
            $('#camera-image').attr("src", meta.attributes.camera_filepath);
            $('#thermal-image').attr("src", meta.attributes.thermal_filepath);
            $('#camera-filepath').html(meta.attributes.camera_filepath);
            $('#thermal-filepath').html(meta.attributes.thermal_filepath);
            $('#camera-filepath').attr("href", meta.attributes.camera_filepath);
            $('#thermal-filepath').attr("href", meta.attributes.thermal_filepath);

            // Update chart
            // chart.data.datasets[0].data = meta.attributes.thermal_history;
            // chart.data.datasets[1].data = meta.attributes.servo_setpoint_history;
            // chart.data.datasets[2].data = meta.attributes.servo_achieved_history;
            // chart.update()

            // Live control
            $('#temperature').html(meta.attributes.temperature);
            $('#fixed-setpoint-output').html(meta.attributes.servo_setpoint);
            $('#temperature-target-output').html(meta.attributes.temperature_target);
            $('#p-coefficient-output').html(meta.attributes.p_coefficient);
            $('#i-coefficient-output').html(meta.attributes.i_coefficient);
            $('#d-coefficient-output').html(meta.attributes.d_coefficient);
            $('#frame-interval-output').html(meta.attributes.interval);


            if (meta.attributes.session_name == undefined) {
                $("#stop").hide();
                $("#start").show();
                $('#session-id').prop("disabled", false);
                $('#session-id-output').html("Enter session ID");
            } else {
                $("#start").hide();
                $("#stop").show();
                $('#session-id').prop("disabled", true);
                $('#session-id-output').html(meta.attributes.session_name);
            }
        }

    });
}


// ------------- UPDATE ON CONNECTION SUCCESS -------------


function connection_success() {
    $("#not-connected").hide();
    $("#connected").show();
    if (connected == false) {
        // Refresh data on first reconnect
        get_all_labels()
        get_all_models()
        connected = true
    }

}

function connection_failed() {
    $("#connected").hide();
    $("#not-connected").show();
    connected = false
}



// ------------- UPDATE ON INITIAL PAGE LOAD -------------


$(document).ready(function() {

    $('#ip-address').attr("placeholder", localStorage.ip_address);

    $("#start").hide();
    $("#stop").hide();

    get_all_labels()
    get_all_models()

    // Refresh page
    setInterval(update, update_interval);

});


// --------------------- FUNCTIONS  ----------------------

function get_all_labels() {
    get("get_all_labels", function(data) {
        // data is a js object 

        let dropdown = $('#select-labels');

        dropdown.empty();
        dropdown.append('<option selected="true" disabled>Select labels</option>');
        dropdown.prop('selectedIndex', 0);

        // Populate dropdown 
        var dataJSON = JSON.parse(data);

        $.each(dataJSON.attributes, function(key, entry) {
            dropdown.append($('<option></option>').attr('value', key).text(key));
            // dropdown.append($('<option></option>').attr('value', entry.label).text(entry.label));
        });

        dropdown.change(function() {

            let key = $(this).val();

            let label_buttons = $('#label-button-group');
            label_buttons.empty();

            $.each(dataJSON.attributes[key], function(key, entry) {

                label_buttons.append($('<button type="button" class="btn btn-outline-primary label-button"></button>').html(entry)); //.html(entry).attr('value', entry)
            });

            $('.label-button').on('click', function() {
                set('set_active_label', $(this).text());
            });

        });

    });
}

function get_all_models() {
    get("get_all_models", function(data) {
        // data is a js object 

        let dropdown = $('#select-model');

        dropdown.empty();

        dropdown.append('<option selected="true" disabled>Select model</option>');
        dropdown.prop('selectedIndex', 0);

        // Populate dropdown
        var dataJSON = JSON.parse(data);

        $.each(dataJSON, function(key, entry) {
            dropdown.append($('<option></option>').attr('value', entry.label).text(entry.label));
        });
    });
}



//---------- ASYNCHRONOUS EVENT PAGE LISTENERS  ----------

$(document).ready(function() {

    // Live labelling

    $('#start').on('click', function() {
        set('start', $('#session-id-input').val());
        $('#session-id-input').val('');
    });

    $('#stop').on('click', function() {
        get("stop", function(foo) {});
    });

    $('#select-model-button').on('click', function() {
        set('set_active_model', $('#select-model').val());
    });

    $('#quit').on('click', function() {
        get("quit", function(foo) {});
    });

    $('#restart').on('click', function() {
        get("restart", function(foo) {});
    });

    $('#pi-shutdown').on('click', function() {
        get("pi_shutdown", function(foo) {});
    });

    $('#pi-restart').on('click', function() {
        get("pi_restart", function(foo) {});
    });


    // Live control

    $('#fixed-setpoint-button').on('click', function() {
        set('set_fixed_setpoint', $('#fixed-setpoint-input').val());
        $('#fixed-setpoint-input').val('');
    });

    $('#hob-off-button').on('click', function() {
        set('set_hob_off', "_");
        $('#fixed-setpoint-input').val('');
    });

    $('#temperature-target-button').on('click', function() {
        set('set_temperature_target', $('#temperature-target-input').val());
        $('#temperature-target-input').val('');
    });

    $('#temperature-hold-button').on('click', function() {
        set('set_temperature_hold', function(foo) {});
        $('#temperature-target-input').val('');
    });


    $('#pid-p-button').on('click', function() {
        set('set_p_coefficient', $('#p-coefficient-input').val());
        $('#p-coefficient-input').val('');
    });

    $('#pid-i-button').on('click', function() {
        set('set_i_coefficient', $('#i-coefficient-input').val());
        $('#i-coefficient-input').val('');
    });

    $('#pid-d-button').on('click', function() {
        set('set_d_coefficient', $('#d-coefficient-input').val());
        $('#d-coefficient-input').val('');
    });

    $('#reset-pid-button').on('click', function() {
        get("set_pid_reset", function(foo) {});
    });

    $('#frame-interval-button').on('click', function() {
        set('set_frame_interval', $('#frame-interval-input').val());
        $('#frame-interval-input').val('');
    });

    $('#min-interval-button').on('click', function() {
        set('set_frame_interval', 0);
        $('#frame-interval-input').val('');
    });



    $('#ip-address-button').on('click', function() {
        localStorage.ip_address = $('#ip-address').val()
        $('#ip-address').attr("placeholder", localStorage.ip_address);
        $('#ip-address').val('');
    });
});