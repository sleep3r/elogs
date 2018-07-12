var datePicker = $('#datepicker').datepicker();
$('#datepicker').on('changeDate', function() {
    $('#my_hidden_input').val(
        $('#datepicker').datepicker('getFormattedDate')
    );
});

function on_form_change(form) {
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: console.log,
        dataType: "json"
    });
}