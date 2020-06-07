// -------------------------------------------------------
// PORTAL.JS COPYRIGHT BEN COBLEY 2020 




// -------------------------------------------------------
// ---------------- APPLICATION VARIABLES ----------------


var endpoint_url = 'http://192.168.0.1:5001/'
if (!localStorage.ip_address) {
    $('#IPmodal').modal('show');
} else {
    var endpoint_url = 'http://192.168.0.' + localStorage.ip_address + ':5001/';
}

var update_interval = 100;
var connected = false;
var previous_message = null;

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

    $('#ip-address-output').html(localStorage.ip_address);
    
    get("error_message", function(data) {

            if (data != "") {
                $("#previous-instruction").html("");
                $("#next-instruction").html("");
                data = data.concat('&nbsp;&nbsp;<span data-feather="alert-circle" style="height: 1.1em; width: 1.1em"></span>');
                $("#current-instruction").html(data);
                feather.replace();
                previous_message = "foo"
            } else {

                get("next_message", function(data) {

                    next = 'Next:&nbsp;'
                    data = next.concat(data);
                    $("#next-instruction").html(data);

                });

                get("previous_message", function(data) {

                    data = data.concat('&nbsp;&nbsp;<span data-feather="check-circle" style="height: 1.1em; width: 1.1em"></span>');
                    $("#previous-instruction").html(data);
                    feather.replace();

                });

                get("current_message", function(data) {
                    // data is a js object 
                    connection_success()

                    // Only refresh when new data
                    if (data == previous_message) {
                        // Update previous meta
                        previous_message = data
                    } else {
                        previous_message = data

                        $("#current-instruction").html(data)
                        console.log("fitty")
                        fitty.fitAll()


                    }

                });
            }

        });

}
// ------------- UPDATE ON CONNECTION SUCCESS -------------


function connection_success() {
    $("#not-connected").hide();
    $('#connected').show();
    $("#current-instruction").show();
    $("#next-instruction").show();
}

function connection_failed() {
    $("#connected").hide();
    $("#not-connected").show();
    $("#previous-instruction").html("Not connected")
    $("#current-instruction").hide();
    $("#next-instruction").hide();

}



// ------------- UPDATE ON INITIAL PAGE LOAD -------------


$(document).ready(function() {

    $('#ip-address').attr("placeholder", localStorage.ip_address);

    // Refresh page
    setInterval(update, update_interval);

});




//---------- ASYNCHRONOUS EVENT PAGE LISTENERS  ----------

$(document).ready(function() {

    // API control

    $('#ip-address-button').on('click', function() {
        localStorage.ip_address = $('#ip-address-input').val();
        $('#ip-address-output').html(localStorage.ip_address);
        $('#ip-address-input').val('');
        endpoint_url = 'http://192.168.0.' + localStorage.ip_address + ':5001/';
    });

    $('#next').on('click', function() {
        set("next", function(foo) {});
    });

    $('#previous').on('click', function() {
        set("previous", function(foo) {});
    });

    $('#stop').on('click', function() {
        set("stop", function(foo) {});
    });


});