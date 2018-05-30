function on_form_change(form) {
    clone_last_line(form);
    clear_empty_lines(form);

    if (!$(form).find()) {

    }

    $.ajax({
        type: 'POST',
        url: $(form).attr('action'),
        data: $(form).serialize(),
        success: console.log,
        dataType: "json"
    });
}

function on_input_change(input) {
    const json = input.dataset.info.replace(/'/g, '"');
    const info = JSON.parse(json);

    if (info.type !== "droplist" ) {
        input.type = info.type;
    }

    if (input.type === "number" && (input.value * 1 < info.min_normal || input.value * 1 > info.max_normal)) {
        $(input).addClass('red').removeClass('black');
    } else {
        $(input).addClass('black').removeClass('red')
    }

    if (info.type === "datalist" ) {
        $(input).removeAttr( "type" );
        $(input).attr('list', 'datalist');

        if ($('#datalist').length == 0) {
            $(input).after('<datalist id="datalist"></datalist>');
            info.options.forEach((name)=>{
                $("#datalist").append("<option>" + name + "</option>");
            })
        }
    }

    if (info.type == "text") {

    }

    $(input).attr('placeholder', info.units);
    $(input).attr('title', info.units);
}


function line_is_empty(tr_line) {
    let filled = 0;
    tr_line.find('input').each(function () {
        if (this.value.trim() !== "") {
            filled++;
        }
    });

    return filled === 0;
}


function clone_last_line(form) {

    const table = $(form).find("table");
    const last_line = table.find(".indexed-line:last");

    if (!line_is_empty(last_line)) {
        let new_last_line = last_line.clone();
        new_last_line.find("input").val("");
        new_last_line.find(".index-input").val(last_line.find(".index-input").val()*1 + 1);
        table.append(new_last_line);
    }
}


function add_first_line(form) {

}


function clear_empty_lines(form) {
    const table = $(form).find("table");

    let last_line = null;
    $(table.find(".indexed-line").get().reverse()).each(function (index) {
        if (line_is_empty($(this))) {
            if (last_line) {
                last_line.remove();
            }
            last_line = this;
        } else {
            return false;
        }
    });
}


$(document).ready(function () {
    document.querySelectorAll(".general-value").forEach(input => { // Adding on_input_change for every input
        on_input_change(input);
    });

    $("form").trigger("input"); // Process initial table data

    String.prototype.trim = function () {
        return this.replace(/^\s*/, "").replace(/\s*$/, "");
    };

    $.ajax({ // Adding getting fields_info from server and saving in to local storage
        type: 'GET',
        url: '/common/fields_info/',
        dataType: "json",
    }).done((res)=>{
        window.localStorage.setItem("fields_info", res)
    });
});
