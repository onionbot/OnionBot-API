// -------------------------------------------------------
// PORTAL.JS COPYRIGHT BEN COBLEY 2020 




// -------------------------------------------------------
// ---------------- APPLICATION VARIABLES ----------------

$('#IPbox').show();

var endpoint_url = 'http://192.168.0.1:5000/'
if (!localStorage.ip_address) {
    $('#IPmodal').modal('show');
} else {
    var endpoint_url = 'http://192.168.0.' + localStorage.ip_address + ':5000/';
}

var update_interval = 100;
var connected = false;
var previous_meta = null;
var filename = location.href.split("/").slice(-1)[0];

if (filename == "control.html") {
    var ctx = document.getElementById('myChart').getContext('2d');
}

if (filename == "labelling.html") {
    $('#label-table').bootstrapTable({
        data: [],
        formatNoMatches: function() {
            return 'Ready to start labelling';
        }
    });

    function badgeFormatter(value) {
        return '<span class="badge badge-light" style="font-size: 17px;">' + value + '</span>'
    }
}

if (filename == "inference.html") {
    $('#inference-table').bootstrapTable({
        data: [],
        formatNoMatches: function() {
            return 'Ready to start inference';
        }
    });

    function badgeFormatter(value) {
        return '<span class="badge badge-light" style="font-size: 17px;">' + value + '</span>'
    }
}



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
        } else {
            // Update previous meta
            previous_meta = data

            meta = JSON.parse(data);

            if (meta.attributes.label_count && filename == "labelling.html") {
                let table_data = []
                for (let [key, value] of Object.entries(meta.attributes.label_count)) {
                    table_data.push({
                        "label": key,
                        "count": value
                    });
                }
                $('#label-table').bootstrapTable('load', table_data);
            }

            if (meta.attributes.classification_data && filename == "inference.html") {
                let table_data = []
                for (let [key, value] of Object.entries(meta.attributes.classification_data)) {
                    console.log(key, value)
                    table_data.push({
                        "model": key,
                        "result": value.label,
                        "probability": value.confidence,
                    });
                }
                $('#inference-table').bootstrapTable('load', table_data);
            }

            // Update key information
            $('#session-id-output').html(meta.attributes.session_ID);
            $('#measurement-id').html(meta.attributes.measurement_ID);

            if (meta.attributes.label) {
                $('#label').html(meta.attributes.label);
            } else {
                $('#label').html("None");
            }


            // Load new images
            $('#camera-image').attr("src", meta.attributes.camera_filepath);
            $('#thermal-image').attr("src", meta.attributes.thermal_filepath);
            $('#camera-link').attr("href", meta.attributes.camera_filepath);
            $('#thermal-link').attr("href", meta.attributes.thermal_filepath);

            // Update chart
            if (filename == "control.html") {
                chart.data.datasets[0].data = meta.attributes.thermal_history;
                chart.data.datasets[1].data = meta.attributes.servo_setpoint_history;
                chart.data.datasets[2].data = meta.attributes.servo_achieved_history;
                chart.update()
            }
            
            // Live control
            $('#temperature').html(meta.attributes.temperature);
            $('#fixed-setpoint-output').html(meta.attributes.servo_setpoint);
            $('#temperature-target-output').html(meta.attributes.temperature_target);
            $('#p-coefficient-output').html(meta.attributes.p_coefficient);
            $('#i-coefficient-output').html(meta.attributes.i_coefficient);
            $('#d-coefficient-output').html(meta.attributes.d_coefficient);
            $('#frame-interval-output').html(meta.attributes.interval);

            if (meta.attributes.session_ID == undefined) {
                $("#stop").hide();
                $("#table-div").hide();
                $("#start").show();
                $('#session-id-input').prop("disabled", false);
                $('#session-id-output').html("None");
            } else {
                $("#start").hide();
                $("#table-div").show();
                $("#stop").show();
                $('#session-id-input').prop("disabled", true);
                $('#session-id-output').html(meta.attributes.session_ID);
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

        let dropdown = $('#select-label');

        dropdown.empty();
        dropdown.append('<option selected="true" disabled>Select from group</option>');
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

            $('#select-label-clear').show();

            $('.label-button').on('click', function() {
                set('set_label', $(this).text());
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

    // API control

    $('#ip-address-button').on('click', function() {
        localStorage.ip_address = $('#ip-address-input').val();
        $('#ip-address-output').html(localStorage.ip_address);
        $('#ip-address-input').val('');
        endpoint_url = 'http://192.168.0.' + localStorage.ip_address + ':5000/';
        IPbox.hide();
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


    // Live labelling

    $('#start').on('click', function() {
        var session_id = $('#session-id-input').val();
        session_id = session_id.trim();
        if (session_id) {
            session_id = session_id.replace(/\s+/g, '_');
            session_id = encodeURIComponent(session_id);
            set('start', session_id);
            $('#session-id-input').val('');
        }
    });

    $('#stop').on('click', function() {
        get("stop", function(data) {
            $('#cloud-location').attr("href", data);
            data = data.replace("https://storage.googleapis.com/", "");
            $('#cloud-location').html(data);
            $('#stopModal').modal('show');
        });
    });

    $('#type-label-button').on('click', function() {
        var new_label = $('#type-label-input').val();
        new_label = new_label.trim();
        if (new_label) {
            new_label = new_label.replace(/\s+/g, '_');
            new_label = encodeURIComponent(new_label);
            set('set_label', new_label);
            $('#type-label-input').val('');
        }
    });

    $('#select-label-clear').on('click', function() {
        set("set_no_label", function(foo) {});
    });

    $('#type-label-clear').on('click', function() {
        set("set_no_label", function(foo) {});
    });

    // Live inference

    $('#select-model-button').on('click', function() {
        set('set_active_model', $('#select-model').val());
    });

});