
$('#btn-set-temp').on('click', function() {
  $.ajax({
    type: "POST",
    url: "http://192.168.0.73:5000/",
    data: {
      action: "set_temp",
      temp: $("#temp").val()
    },
    success: function(data) {
      alert(data);
    },
  });
});
