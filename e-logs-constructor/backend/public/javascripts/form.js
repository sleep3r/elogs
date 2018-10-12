$("#form").submit(function(e) {
    e.preventDefault();
    // let data = $(this).serialize()
    let data = new FormData(this)
    $.ajax({
        url: '/import',
        type: 'POST',
        data: data,
        processData: false,
        contentType: false,
        success: function(data) {
            console.log(data)
        }
    })
})
