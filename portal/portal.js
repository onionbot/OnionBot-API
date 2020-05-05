// -------------------------------------------------------
// PORTAL.JS COPYRIGHT BEN COBLEY 2020 




// -------------------------------------------------------
// ---------------- APPLICATION VARIABLES ----------------

var endpoint_url = 'http://192.168.0.70:5000/';
var update_interval = 100;
var connected = false;
var ctx = document.getElementById('myChart').getContext('2d');


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
    // console.log("Update page called")

    get("get_latest_meta", function(data) {
        // data is a js object 

        connection_success()
        data = JSON.parse(data);

        // Update key information
        $('#session-name').html(data.attributes.session_name);
        $('#active-label').html(data.attributes.active_label);
        $('#measurement-id').html(data.attributes.measurement_id);
        $('#time-stamp').html(data.attributes.time_stamp);

        // Updata live data


        // Load new images
        $('#camera-image').attr("src", data.attributes.camera_filepath);
        $('#thermal-image').attr("src", data.attributes.thermal_filepath);
        $('#camera-filepath').html(data.attributes.camera_filepath);
        $('#thermal-filepath').html(data.attributes.thermal_filepath);
        $('#camera-filepath').attr("href", data.attributes.camera_filepath);
        $('#thermal-filepath').attr("href", data.attributes.thermal_filepath);



        chart.data.datasets[0].data = data.attributes.thermal_history;
        chart.data.datasets[1].data = data.attributes.servo_setpoint_history;
        chart.data.datasets[2].data = data.attributes.servo_achieved_history;
        chart.update()



        $('#fixed-setpoint').attr("placeholder", data.attributes.servo_setpoint);
        $('#temperature-target').attr("placeholder", data.attributes.temperature_target);
        // $('#camera-sleep').attr("placeholder", data.attributes.camera_sleep);

        if(data.attributes.session_name == undefined){
            $("#stop").hide();
            $("#start").show();
            $('#session-id').prop("disabled", false);
            $('#session-id').attr("placeholder", "Enter session ID");
        }   else {
            $("#start").hide();
            $("#stop").show();
            $('#session-id').prop("disabled", true);
            $('#session-id').attr("placeholder", data.attributes.session_name);
        }
    
    });
}


// ------------- UPDATE ON CONNECTION SUCCESS -------------


function connection_success() {
    $('#connection-monitor').css("background-color", "green");
    if(connected == false){
    get_all_labels()
    get_all_models()
    connected = true

    }
}

function connection_failed() {
    $('#connection-monitor').css("background-color", "yellow");
    connected = false
}



// ------------- UPDATE ON INITIAL PAGE LOAD -------------


$(document).ready(function() {

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

            //console.log(dataJSON);
            //console.log(dataJSON.attributes);

            let label_buttons = $('#label-button-group');
            label_buttons.empty();

            $.each(dataJSON.attributes[key], function(key, entry) {
                console.log(entry);

                label_buttons.append($('<button type="button" class="btn btn-secondary label-button"></button>').html(entry)); //.html(entry).attr('value', entry)
            });

            $('.label-button').on('click', function() {
                console.log($(this).text());
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

    $('#start').on('click', function() {

        set('start', $('#session-id').val());
        set('set_chosen_labels', $('#select-labels').val());
    });

    $('#stop').on('click', function() {
        get("stop", function(foo) {
            console.log("Stopping")
        });
    });

    $('#connection-monitor').on('click', function() {
        get("quit", function(foo) {
            console.log("Quitting")
        });
    });

    $('#select-model-button').on('click', function() {
        set('set_active_model', $('#select-model').val());
    });

    $('#fixed-setpoint-button').on('click', function() {
        set('set_fixed_setpoint', $('#fixed-setpoint').val());
        $('#fixed-setpoint').attr("placeholder", "Updating...");
        $('#fixed-setpoint').val('');
    });

    $('#temperature-target-button').on('click', function() {
        set('set_temperature_target', $('#temperature-target').val());
        $('#temperature-target').attr("placeholder", "Updating...");
        $('#temperature-target').val('');
    });

    $('#pid-button').on('click', function() {
        var coefficients = [('#p-coefficient').val(), ('#i-coefficient').val(), ('#d-coefficient').val()]
        set('set_pid_coefficients', coefficients);
        $('#p-coefficient').attr("placeholder", "Updating...");
        $('#p-coefficient').val('');
        $('#i-coefficient').attr("placeholder", "Updating...");
        $('#i-coefficient').val('');
        $('#d-coefficient').attr("placeholder", "Updating...");
        $('#d-coefficient').val('');
    });

    $('#hob-off-button').on('click', function() {
        set('set_hob_off', "_");
        $('#fixed-setpoint').attr("placeholder", "Updating...");
        $('#fixed-setpoint').val('');
    });

    $('#camera-sleep-button').on('click', function() {
        set('set_camera_sleep', $('#camera-sleep').val());
    });
});




