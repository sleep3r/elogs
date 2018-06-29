/*jshint esversion: 6 */


function on_form_change(form) {
    console.log("on_form_change()");
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

function add_message(input) {
    console.log("on_input_change()");
    const json = input.dataset.info.replace(/'/g, '"');
    const info = JSON.parse(json);

    if (input.type === "number" && (input.value * 1 < info.min_normal || input.value * 1 > info.max_normal)) {
        $(input).addClass('red').removeClass('black');
        $.ajax({
            url: "/common/messages/add",
            type: 'POST',
            data: { 'check': true, 'field_name': input.name, 'field_value': input.value, 
                    'table_name': $(input).attr('table-name'), 'journal_page': $(input).attr('journal-page'),
                    'index':$(input).attr('index') },
            success: function (json) {
                if (json.result) {
                    console.log(json.result)
                }
            }
        });
        
    } else{
        $.ajax({
            url: "/common/messages/del",
            type: 'POST',
            data: { 'check': true, 'field_name': input.name, 
                    'table_name': $(input).attr('table-name'), 'journal_page': $(input).attr('journal-page'),
                    'index':$(input).attr('index') },
            success: function (json) {
                if (json.result) {
                    console.log(json.result)
                }
            }
        });
    }

}

function on_input_change(input) {
    console.log("on_input_change()");
    const json = input.dataset.info.replace(/'/g, '"');
    const info = JSON.parse(json);

    if (info.type !== "droplist") { // for dropdowns
        input.type = info.type;
    }

    if (input.type === "number" && (input.value * 1 < info.min_normal || input.value * 1 > info.max_normal)) {
        $(input).addClass('red').removeClass('black');
    } else {
        $(input).addClass('black').removeClass('red')
    }

    if (info.type === "datalist") {
        $(input).removeAttr("type");
        $(input).attr('list', 'datalist');

        if ($('#datalist').length == 0) {
            $(input).after('<datalist id="datalist"></datalist>');
            info.options.forEach((name) => {
                $("#datalist").append("<option>" + name + "</option>");
            })
        }

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
        new_last_line.find(".index-input").val(last_line.find(".index-input").val() * 1 + 1);
        table.append(new_last_line);
    }
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


function showPopup(field, event) {
    let comment_id = field
    let comment_input_id = comment_id + "_input";
    comment = document.getElementById(comment_id);
    comment_input = document.getElementById(comment_input_id);
    input = $(comment).siblings()[0];

    $(input).css(
        "background",
        "radial-gradient(white 80%, #24A48A)"
    );
    cell = $(comment).parent();
    // if (cell.is(':last-child')) {
    //     $(comment).addClass("show-extreme")
    // }
    $(comment).addClass("show");
    $(comment_input).focus();
}


function hidePopups(field) {
    let comment_id = field;
    comment = document.getElementById(comment_id);
    input = $(comment).siblings()[0];
    $(input).css(
        "background",
        "white"
    );
    $(".popup-comment-content").removeClass("show");
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
    }).done((res) => {
        window.localStorage.setItem("fields_info", res)
    });

    $('[readonly]').focus(function () { // delete cursor for readonly fields
        $('[readonly]').blur();
    });


    $('.indexed-line:has([readonly]):last').filter((index, line) => { // deleting empty line for readonly cases
        return line_is_empty($(line));
    }).remove();


    let validate = $("input[name='validate']").attr("value");
    console.log(validate);
    if (validate === "True") {
        console.log('check');
        $('.indexed-line').removeClass('indexed-line')
    }


});
