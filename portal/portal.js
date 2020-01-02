'use strict';


/*******************************************************/
/*************** Application variables *****************/

var endpoint_url = 'http://192.168.0.73:5000/';
var update_interval = 500;
/*******************************************************/



function set(function_name, argument) {
  $.ajax({
    type: 'POST',
    url: endpoint_url,
    data: {
      action: function_name,
      value: argument
    },
    success: function(confirmation) {
      console.log(confirmation);
    },
  });
}


function get(function_name, callback) {
  $.ajax({
    type: 'POST',
    url: endpoint_url,
    data: {
      action: function_name,
    },
    success: callback 
  });
}

function update() {


  get("get_latest_meta", function( data ) {
    // data is a js object 

    data = JSON.parse(data);
    
    console.log(data)
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

  });
  
}


$(document).ready(function() {
  
  $("#stop").hide();

  // Event listeners for page interactions 

  get("get_all_labels", function( data ) {
    // data is a js object 

    var label_json
    label_json = data //JSON.parse(data);

    let dropdown = $('#select-labels');

    dropdown.empty();

    dropdown.append('<option selected="true" disabled>Select labels</option>');
    dropdown.prop('selectedIndex', 0);

    // Populate dropdown with list of provinces
    var dataJSON = JSON.parse(data);

    $.each(dataJSON, function (key, entry) {
      dropdown.append($('<option></option>').attr('value', entry.label).text(entry.label));
    });

    
  });



  $('#start').on('click', function() {
    
    set('start', $('#session-id').val());

    set('set_chosen_labels', $('#select-labels').val());

    $("#start").hide();
    $("#stop").show();

    // Refresh page
    setInterval(update, update_interval);
  });

  $('#stop').on('click', function() {
    
    get("stop", function( foo ) {
      console.log("Stopping")


      $("#stop").hide();
      $("#start").show();
      clearInterval(update)
      update()

    });

  });


});

