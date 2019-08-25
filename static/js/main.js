PREVIEW_IMAGE_HEIGHT = 300;

jQuery.ajaxSetup({
  beforeSend: function() {
     $('#loading').removeClass('hidden');
  },
  complete: function(){
     $('#loading').addClass('hidden');
  },
  success: function() {
    $('#loading').addClass('hidden');
  }
});

$('#btn-upload-file, #btn-upload-another').on('click', function(e) {
  e.preventDefault();
  
  $('#file').click();
});

// Show the selected image to the UI before uploading
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    
    reader.onload = function(e) {
      $('#preview-image').attr('src', e.target.result).css('height', PREVIEW_IMAGE_HEIGHT);
    }
    
    reader.readAsDataURL(input.files[0]);

    process_upload_another()
  }
}

$("#file").change(function() {
  $('#preview-image').removeClass('hidden');
  readURL(this);
});

function process_upload_another() {
  $('#btn-upload-another, #btn-submit-file').removeClass('hidden');
  $btn_upload_file = $('#btn-upload-file');
  $btn_upload_file.addClass('relative');

  $upload_another = $btn_upload_file.find('span');
  $upload_another.addClass('hidden');
  
  $('.box-predict-results').addClass('hidden');
  $('.box-intro-inner').removeClass('hidden')
  $('#form-predict-correction .button').removeClass('hidden');
  $('.box-predict-correction').addClass('hidden');
  $('#thank-you').text('');
}

// Upload image using AJAX
let my_form = document.getElementById('form-upload-image');
$('#btn-submit-file').on('click', function(e) {
  e.preventDefault();
  $('#form-upload-image').trigger('submit');
});
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
      $('#predict-result').text(data['label']);
      $('#predict-probs').text(data['probs'] + '%');
      $('#upload-file-path').val(data['upload_file_path']);
      
      $('#btn-submit-file').addClass('hidden')
      $('.box-intro').addClass('predict-results')
      $('.box-intro-inner').addClass('hidden')
      $('.box-predict-correction, .box-predict-results').removeClass('hidden')
    }
  });
});

// Handle Predict Correction
$('#form-predict-correction .btn-correction').on('click', function(e) {
  e.preventDefault();

  label = $(this).attr('data-label')

  handle_predict_correction(label)
})

function handle_predict_correction(label) {
  let correction_form = document.getElementById('form-predict-correction')

  let form_data = new FormData(correction_form);
  form_data.append('correction-label', label)

  $.ajax({
    type: 'POST',
    url: '/predict-correction/',
    processData: false,
    contentType: false,
    data: form_data,
    success: function(data) {
      $('#form-predict-correction .button').addClass('hidden')
      $('#thank-you').text(data['message']);
    }
  });
};