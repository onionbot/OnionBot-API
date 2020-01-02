'use strict';


/*******************************************************/
/*************** Application variables *****************/

var endpoint_url = 'http://192.168.0.73:5000/';
var refresh_interval = 500;

var meta_url;

/*******************************************************/


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


function execute(function_name) {
  $.ajax({
    type: 'POST',
    url: endpoint_url,
    data: {
      action: function_name,
    },
    success: function(confirmation) {
      console.log(confirmation);
    },
  });
}


function refresh() {
    
  var new_meta_url = get('get_latest_meta', update);
  
}


function update(new_meta_url) {

  if (new_meta_url != meta_url) {

    meta_url = new_meta_url;

    // meta_url has changed so update page information 

    $.getJSON(meta_url, function( data ) {
      // data is a js object 

      console.log(data);
      
      $('#session_name').html(data.session_name);
      $('#label').html(data.label);
      $('#camera_prediction').html(data.camera_prediction);
      $('#thermal_prediction').html(data.thermal_prediction);
      $('#measurement_id').html(data.measurement_id);
      $('#time_stamp').html(data.time_stamp);
      $('#temperature').html(data.temperature);
      $('#camera_filepath').html(data.camera_filepath);
      $('#thermal_filepath').html(data.thermal_filepath);
      $('#camera_filepath').href = data.camera_filepath; $('#camera_filepath').html = data.camera_filepath;
      $('#thermal_filepath').href = data.thermal_filepath; $('#thermal_filepath').html = data.thermal_filepath;
      $('#camera_image').src = data.camera_filepath;
      $('#thermal_image').src = data.thermal_filepath;

    });
  }
}


$(document).ready(function() {
  

  //   init() {
  //     var dropdownOptions;
  //     // call to python script, save repsonse to dropdownOptions 
  //       // in callback function (once response has been obtained):
  //       // populate dropdown with jQuery

  //   }


  // });



  // Event listeners for page interactions 


  $('#start').on('click', function() {
    
    set('start', $('#session-id').val());

    set('set_chosen_labels', $('#labels').val());
    
    set('set_active_label', 'testlabeljson')
    set('set_active_model', 'testmodeljson')

    // Show hidden boxes


    // Refresh stuff
    setInterval(refresh, refresh_interval);
  });



});

