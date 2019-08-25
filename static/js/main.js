// Show the selected image to the UI before uploading
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

// Upload image using AJAX
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
      console.log(data['upload_file_path'])
      $('#result').text('Predicted Output: ' + data['label']);
      $('#probs').text('Probability: ' + data['probs']);
      $('#upload-file-path').val(data['upload_file_path']);
    }
  });
});

$('#form-predict-correction .btn-correction').on('click', function(e) {
  e.preventDefault();

  label = $(this).attr('data-label')

  handle_predict_correction(label)
})

function handle_predict_correction(label) {
  let correction_form = document.getElementById('form-predict-correction')

  let form_data = new FormData(correction_form);
  form_data.append('correction-label', label)

  console.log(label)

  $.ajax({
    type: 'POST',
    url: '/predict-correction/',
    processData: false,
    contentType: false,
    data: form_data,
    success: function(data) {
      $('#thank-you').text(data['message']);
    }
  });
};

// $('#form-predict-correction').submit(function(e) {
//   e.preventDefault();
  
//   let form_data = new FormData(correction_form);
//   form_data.append('correction-label', $('#form-predict-correction correction-label'))
//   $.ajax({
//     type: 'POST',
//     url: '/predict-correction/',
//     processData: false,
//     contentType: false,
//     data: form_data,
//     success: function(data) {
//       $('#thank-you').text('THANK YOU FOR YOUR CORRECTION!!!');
//     }
//   });
// });