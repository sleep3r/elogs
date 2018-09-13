$(document).ready(function () {
    $('input[type="time"]').addClass('clockpicker').clockpicker(
        {
            autoclose: true,
            'default': 'now'
        }
    )
})