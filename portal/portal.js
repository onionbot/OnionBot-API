"use strict";

$('#btn-set-temp').on('click', function() {
  $.ajax({
    type: "POST",
    url: "http://192.168.0.73:5000/",
    data: {
      action: "set_hob",
      temp: $("#temp").val()
    },
    success: function(data) {
      alert(data);
    },
  });
});


function myFn(arg1, arg2) {
  alert(arg1);
  $("#btn-set-temp").html("button");
  $(".btn").html("button");
}


function refresh() {
  $.getJSON("url goes here ?key=skdhflskfhldf", function(data) {
    // data is a js object 
    console.log(data.hobtemp);
  });
}


setInterval(refresh, 500);
