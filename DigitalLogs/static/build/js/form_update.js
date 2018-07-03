/*jshint esversion: 6 */


var send_form =  _.debounce((form) => {
    console.log("send_form()");
    $.ajax({
        type: 'POST',
        url: $(form).attr('action'),
        data: $(form).serialize(),
        success: console.log,
        dataType: "json"
    });
}, 1500);


function on_form_change(form) {
    console.log("on_form_change()");
    clone_last_line(form);
    clear_empty_lines(form);

    send_form(form);
}


var add_message_debounced = _.debounce((input) => {
    console.log("add_message_debounced()");
    const json = input.dataset.info.replace(/'/g, '"');
    const info = JSON.parse(json);

    if (input.type === "number" && (input.value * 1 < info.min_normal || input.value * 1 > info.max_normal)) {
        $.ajax({
            url: "/common/messages/add",
            type: 'POST',
            data: { 'check': true, 'field_name': input.name, 'field_value': input.value,
                    'table_name': $(input).attr('table-name'), 'journal_page': $(input).attr('journal-page'),
                    'index':$(input).attr('index') },
            success: function (json) {
                if (json && json.result) {
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
                if (json && json.result) {
                    console.log(json.result)
                }
            }
        });
    }
}, 1500);


function add_message(input) {
    console.log("add_message()");
    add_message_debounced(input)
}


function on_input_change(input) {
    console.log("on_input_change()");
    const json = input.dataset.info.replace(/'/g, '"');
    const info = JSON.parse(json);

    if (info.type !== "droplist") { // for dropdowns
        input.type = info.type;
    }

    if (input.type === "number") {
        if (input.value * 1 < info.min_normal || input.value * 1 > info.max_normal) {
            $(input).addClass('red').removeClass('black');
        } else {
            $(input).addClass('black').removeClass('red')
        }
    } else if (info.type === "datalist") {
        $(input).removeAttr("type");
        $(input).attr('list', 'datalist');

        if ($('#datalist').length === 0) {
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


function showValidatePopup(input) {
    comment = $(input).siblings()[0];
    comment_input = $(comment).children()[1];

    $(input).css(
        "background",
        "radial-gradient(white 80%, #24A48A)"
    );
    $(comment).addClass("show");
    $(comment_input).focus();
}


function showViewPopup(icon) {
    input = $(icon).siblings()[0];
    comment = $(icon).siblings()[1];
    comment_input = $(comment).children()[1];

    $(input).css(
        "background",
        "radial-gradient(white 80%, #24A48A)"
    );
    $(comment).addClass("show");
}


function hidePopups() {
    $(".general-value").css(
        "background",
        "white"
    );
    $(".popup-comment-content").removeClass("show");
}

function hidePopusOnMouseUp(event) {
    let active_comment = $(".popup-comment-content.show")[0];
    console.log(active_comment);
    if (active_comment) {
        let active_input = $(active_comment).siblings()[0];
        let hideFlag = !(
            event.target == active_input ||
            event.target == active_comment ||
            $.contains( active_comment, event.target));
        if (hideFlag) {
            hidePopups();
        }
    }
}

function addCommentNotification(input) {
    comment = $(input).siblings()[0];
    comment_notification = $(input).siblings()[1];
    comment_input = $(comment).children()[1];
    console.log($(comment_input).text());
    if ($(comment_input).text()) {
        $(comment_notification).addClass("show")
    }
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
    let view = $("input[name='view']").attr("value");
    if (validate === "True") {
        $('.indexed-line').removeClass('indexed-line')
    }
    document.addEventListener('mouseup', hidePopusOnMouseUp);
    if (view === "True") {
        document.querySelectorAll(".general-value").forEach(addCommentNotification)
    }


});
