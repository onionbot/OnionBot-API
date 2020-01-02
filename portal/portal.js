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
    
  //var new_meta_url = get('get_latest_meta', update);
  update();
  
}


function update() {


  // meta has changed so update page information 

  get("get_latest_meta", function( data ) {
    // data is a js object 

    data = JSON.parse(data);

    console.log(data);
    $('#session-name').html(data.session_name);
    $('#label').html(data.label);
    $('#camera-prediction').html(data.camera_prediction);
    $('#thermal-prediction').html(data.thermal_prediction);
    $('#measurement-id').html(data.measurement_id);
    $('#time-stamp').html(data.time_stamp);
    $('#temperature').html(data.temperature);
    $('#camera-filepath').html(data.camera_filepath);
    $('#thermal-filepath').html(data.thermal_filepath);
    $('#camera-filepath').attr("href", data.camera_filepath);
    $('#thermal-filepath').attr("href", data.thermal_filepath);
    $('#camera-image').attr("src", data.camera_filepath);
    $('#thermal-image').attr("src", data.thermal_filepath);

  });
  
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

