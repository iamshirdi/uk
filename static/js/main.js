$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
	$('.loader2').hide();
    $('#result').hide();
	$('#result2').hide();
	$('.image-section2').hide();



    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });
	

	$("#imageUpload2").change(function () {
        $('.image-section2').show();
        $('#btn-predict2').show();
        $('#result2').text('');
        $('#result2').hide();
        readURL(this);
    });
	

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Model Predicted : ' + data);
                console.log('Success!');
            },
        });
    });
	
	// Predict2
    $('#btn-predict2').click(function () {
        var form_data2 = new FormData($('#upload-file2')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader2').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict2',
            data: form_data2,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader2').hide();
                $('#result2').fadeIn(600);
                $('#result2').text(' Model Predicted : ' + data);
                console.log('Success!');
            },
        });
    });


});
