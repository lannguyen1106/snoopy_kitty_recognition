$(document).ready(function() {

  
});

let my_form = document.getElementById('form-upload-image')
$('#form-upload-image').submit(function(e) {
  e.preventDefault();
  
  let form_data = new FormData(my_form);

  $.ajax({
    type: 'POST',
    url: '/upload-image/',
    processData: false,
    contentType: false,
    data: form_data,
    success: function(data) {
      $('#result').text('Predicted Output: ' + data['label']);
      $('#probs').text('Probability: ' + data['probs']);
    }
  });
});

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    
    reader.onload = function(e) {
      $('#preview-image').attr('src', e.target.result);
    }
    
    reader.readAsDataURL(input.files[0]);
  }
}

$("#file").change(function() {
  readURL(this);
});