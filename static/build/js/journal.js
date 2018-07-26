class Journal {

    constructor() {
        this.start = null;
    }

    static focusTo(element) {
        let input = element.getElementsByClassName('form-control')[0];
        if (input) {
            if (input.getAttribute('data-pagmode') === 'edit') {
                input.focus();
                input.select();
            }
            if (input.getAttribute('data-pagmode') === 'validate') {
                hidePopups();
                showValidatePopup(input)
            }
        }
        selectedElement = element;
    }

    static send_all_forms() {

        for (let form of $("form.elog-table-form").get()) {
            $.ajax({
                type: 'POST',
                url: $(form).attr('action'),
                data: $(form).serialize(),
                dataType: "json",
                success: function (data) {
                    $("#async").hide();
                    $("#sync").show();
                }
            });
        }
    }

    static onReady() {
        document.querySelectorAll(".general-value").forEach(input => { // Adding on_input_change for every input
            Cell.on_input_change(input);
        });

        let edit = $("input[name='edit']").attr("value");
        let validate = $("input[name='validate']").attr("value");
        let view = $("input[name='view']").attr("value");


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

        let lines = new Lines();
        $('.indexed-line:has([readonly]):last').filter((index, line) => { // deleting empty line for readonly cases
            return lines.line_is_empty($(line));
        }).remove();

        if (validate === "True") {
            $('.indexed-line').removeClass('indexed-line')
        }
        document.addEventListener('mouseup', PopUp.hideOnMouseUp);
        if (view === "True" || validate === "True") {
            document.querySelectorAll(".popup-comment-content > textarea").forEach(Cell.markCommented)
        }

        $(".table-comment-wrapper").on('shown.bs.collapse', Comment.focus);

        $("#sync").show();

        document.onkeydown = onKeyDownAction;

        window.addEventListener("beforeunload", function (e) {
            Journal.send_all_forms();
        }, false);
    }

    static addMessage(msg) {

        let debounce = _.debounce((input) => {
                const json = input.dataset.info.replace(/'/g, '"');
                const info = JSON.parse(json);

                if (input.type === "number" && (input.value * 1 < info.min_normal || input.value * 1 > info.max_normal)) {
                    $.ajax({
                        url: "/common/messages/create/critical_value/",
                        type: 'POST',
                        data: {
                            'check': true, 'field_name': input.name, 'field_value': input.value,
                            'table_name': $(input).attr('table-name'), 'journal_page': $(input).attr('journal-page'),
                            'index': $(input).attr('index')
                        },
                        success: function (json) {
                            if (json && json.result) {
                                // console.log(json.result)
                            }
                        }
                    });
                } else {
                    $.ajax({
                        url: "/common/messages/update/critical_value/",
                        type: 'POST',
                        data: {
                            'check': true, 'field_name': input.name,
                            'table_name': $(input).attr('table-name'), 'journal_page': $(input).attr('journal-page'),
                            'index': $(input).attr('index')
                        },
                        success: function (json) {
                            if (json && json.result) {
                                // console.log(json.result)
                            }
                        }
                    });
                }
            },
            300);

        debounce(msg)
    }

}


class Comment {

    static add(input) {
        _.debounce((textarea) => {
            $.ajax({
                url: "/common/messages/create/comment/",
                type: 'POST',
                data: {
                    'check': true, 'field_name': $(textarea).attr('name'), 'comment_text': $(textarea).val(),
                    'table_name': $(textarea).attr('table-name'), 'journal_page': $(textarea).attr('journal-page'),
                    'index': $(textarea).attr('index')
                },
                success: function (json) {
                    if (json && json.result) {
                        // console.log(json.result)
                    }
                }
            });
        }, 300)(input);
    }

    static collapse(element) {
        let container = $(element).next();
        container.collapse('toggle');
    }

    static focus(event) {
        $(event.target).children(".table-comment").focus();
    }

}
