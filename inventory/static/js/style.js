// Prevent button from multiple clicks
document.getElementById('submit-btn').addEventListener('click', function() {
    // Disable the button to prevent multiple clicks
    this.disabled = true;
    // Optionally, you can change the button text to indicate processing
    $('#submit-btn').attr('disabled', true).html('<i class="fas fa-spinner fa-pulse"></i> Processing...');
    this.form.submit();
});



// hide error messages
$(document).ready(function(){
    // Hide error message when user starts typing in any input field
    $('input, select').on('input', function() {
        $(this).closest('.form-group').find('.text-danger').fadeOut();
    });
});

