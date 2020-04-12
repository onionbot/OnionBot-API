
// -------------------------------------------------------
// ---------------- APPLICATION VARIABLES ----------------

var endpoint_url = 'http://192.168.0.70:5000/';
var update_interval = 500;



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


function connection_success() {
    $('#connection-monitor').css("background-color", "green");
}


function connection_failed() {
    $('#connection-monitor').css("background-color", "yellow");
}




// ------------- ASYCHRONOUS UPDATE PAGE -------------

function update() {

    console.log("Update page called")

    get("get_latest_meta", function(data) {
        // data is a js object 

        connection_success()
        data = JSON.parse(data);

        $('#session-name').html(data.attributes.session_name);
        $('#active-label').html(data.attributes.active_label);
        $('#active-model').html(data.attributes.active_model);
        $('#camera-prediction').html(data.attributes.camera_prediction);
        $('#thermal-prediction').html(data.attributes.thermal_prediction);
        $('#measurement-id').html(data.attributes.measurement_id);
        $('#time-stamp').html(data.attributes.time_stamp);
        $('#temperature').html(data.attributes.temperature);
        $('#camera-filepath').html(data.attributes.camera_filepath);
        $('#thermal-filepath').html(data.attributes.thermal_filepath);
        $('#camera-filepath').attr("href", data.attributes.camera_filepath);
        $('#thermal-filepath').attr("href", data.attributes.thermal_filepath);
        $('#camera-image').attr("src", data.attributes.camera_filepath);
        $('#thermal-image').attr("src", data.attributes.thermal_filepath);
        $('#hob-setpoint').attr("placeholder", data.attributes.hob_setpoint);
        $('#camera-sleep').attr("placeholder", data.attributes.camera_sleep);
    });

    // get("get_temperature_window", function(data) {
    //     console.log(data)
    //     // chart.update();
    // });

}




// -------- EVENT LISTENERS FOR PAGE INTERACTION ---------

$(document).ready(function() {

    $("#stop").hide();

    // Refresh page
    setInterval(update, update_interval);

    $('#start').on('click', function() {

        set('start', $('#session-id').val());

        set('set_chosen_labels', $('#select-labels').val());

        $("#start").hide();
        $("#stop").show();

    });

    $('#stop').on('click', function() {

        get("stop", function(foo) {
            console.log("Stopping")

            $("#stop").hide();
            $("#start").show();

        });

    });

    get("get_all_labels", function(data) {
        // data is a js object 

        var label_json
        label_json = data //JSON.parse(data);

        let dropdown = $('#select-labels');

        dropdown.empty();
        dropdown.append('<option selected="true" disabled>Select labels</option>');
        dropdown.prop('selectedIndex', 0);

        // Populate dropdown with list of provinces
        var dataJSON = JSON.parse(data);

        $.each(dataJSON, function(key, entry) {
            dropdown.append($('<option></option>').attr('value', entry.label).text(entry.label));
        });


    });

    get("get_all_models", function(data) {
        // data is a js object 

        var label_json
        label_json = data //JSON.parse(data);

        let dropdown = $('#select-model');

        dropdown.empty();

        dropdown.append('<option selected="true" disabled>Select model</option>');
        dropdown.prop('selectedIndex', 0);

        // Populate dropdown with list of provinces
        var dataJSON = JSON.parse(data);

        $.each(dataJSON, function(key, entry) {
            dropdown.append($('<option></option>').attr('value', entry.label).text(entry.label));
        });


    });


    $('#label-button1').on('click', function() {
        set('set_active_label', $('#label-button1').text());
    });
    $('#label-button2').on('click', function() {
        set('set_active_label', $('#label-button2').text());
    });
    $('#label-button3').on('click', function() {
        set('set_active_label', $('#label-button3').text());
    });

    $('#select-model-button').on('click', function() {
        set('set_active_model', $('#select-model').val());
    });

    $('#hob-setpoint-button').on('click', function() {
        set('set_hob_setpoint', $('#hob-setpoint').val());
    });

    $('#hob-off-button').on('click', function() {
        set('set_hob_off', "_");
    });

    $('#camera-sleep-button').on('click', function() {
        set('set_camera_sleep', $('#camera-sleep').val());
    });


});