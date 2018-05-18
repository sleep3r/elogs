function on_form_change(form) {
    $.ajax({
        type: 'POST',
        url: $(form).attr('action'),
        data: $(form).serialize(),
        success: console.log,
        dataType: "json"
    });

    // clone_last_line(form)
}

function on_input_change(input) {
    const json = input.dataset.info.replace(/'/g, '"');
    const info = JSON.parse(json);
    if (input.type === "number" && (input.value * 1 < info.min_normal || input.value * 1 > info.max_normal)) {
        $(input).addClass('red').removeClass('black');
    } else {
        $(input).addClass('black').removeClass('red')
    }

    $(input).attr('placeholder', info.units);
    $(input).attr('title', info.units);
}

function clone_last_line(from) {
    const table = $(form).find("table");
    const last_line = table.find("tr:last");

    let filled = 0;
    last_line.find('input').each(function () {
        if (this.value !== "") {
            filled++;
        }
    });

    if (filled === 0) {
        last_line.clone().appendTo(table);
    }
}

$(document).ready(function () {
    document.querySelectorAll(".general-value").forEach(input => {
        on_input_change(input);
    });
})