$(document).ready(function() {

  
});

$(document).on('submit', '#form-upload-image', function(e) {
  e.preventDefault();

  var form_data = new FormData($('#form-upload-image')[0]);

  $.ajax({
    type: 'POST',
    url: '/upload-image/',
    processData: false,
    contentType: false,
    data: form_data,
    success: function(data) {
      $('#result').text('Predicted Output: ' + data);
    }
  });
});