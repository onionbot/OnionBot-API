'use strict';

// $('#btn-set-temp').on('click', function() {
//   $.ajax({
//     type: 'POST',
//     url: 'http://192.168.0.73:5000/',
//     data: {
//       action: 'set_hob',
//       temp: $('#temp').val()
//     },
//     success: function(data) {
//       alert(data);
//     },
//   });
// });


$(document).ready(function() {
  

  init() {
    var dropdownOptions;
    // call to python script, save repsonse to dropdownOptions 
      // in callback function (once response has been obtained):
      // populate dropdown with jQuery

  }


});


$('#start').on('click', function() {
  
  set('set_chosen_labels', $('#labels').val());
  // Show hidden boxes
  execute('start');
  // Refresh stuff
  setInterval(refresh, 500);

}

function refresh() {
  
  var meta_url; 
  meta_url = get('get_latest_meta');
  $.getJSON(meta_url, function(data) {
    // data is a js object 
    
    $('#session_name').html(data.session_name);
    $('#label').html(data.label);
    $('#camera_prediction').html(data.camera_prediction);
    $('#thermal_prediction').html(data.thermal_prediction);
    $('#measurement_id').html(data.measurement_id);
    $('#time_stamp').html(data.time_stamp);
    $('#temperature').html(data.temperature);
    $('#camera_image').src = data.camera_filepath;
    $('#thermal_image').src = data.thermal_filepath;

  });
}



function set(function_name, argument) {
  $.ajax({
    type: 'POST',
    url: 'http://192.168.0.73:5000/',
    data: {
      func: function_name,
      arg: argument
    },
    success: function(confirmation) {
      return confirmation;
    },
  });
}

function get(function_name) {
  $.ajax({
    type: 'POST',
    url: 'http://192.168.0.73:5000/',
    data: {
      func: function_name,
    },
    success: function(data) {
      return data;
    },
  });
}


function execute(function_name) {
  $.ajax({
    type: 'POST',
    url: 'http://192.168.0.73:5000/',
    data: {
      func: function_name,
    },
    success: function(confirmation) {
      return confirmation;
    },
  });
}


