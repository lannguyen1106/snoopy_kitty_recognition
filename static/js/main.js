$(document).ready(function() {
  console.log("Hello Kitty!")

  $("#fileupload").dropzone({ url: "/file/post" });

  /*
  function handle_upload(e) {
    console.log('Upload File Stating!');
    // console.log(SCRIPT_ROOT)

    var formData = new FormData();
    var img = $('#upload')[0].files[0];

    formData.append("file", img)

    console.log(img)

    try {
      $.ajax({
        type: "POST",
        url: "/upload/",
        data: formData,
        success: function(data){
          console.log('Success')
          $('#result').html('<img src=' + data + ' alt="" />');
        }
      });
    } catch (error) {
      console.log(error)
    } finally {}
  }

  $('form').on('submit', handle_upload);

  // $('#button_upload').click(handle_upload);
  */

});