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
            console.log('adding on_input_change', input);
            Cell.on_input_change(input);
        });

        let edit = $("input[name='edit']").attr("value");
        let validate = $("input[name='validate']").attr("value");
        let view = $("input[name='view']").attr("value");


        String.prototype.trim = function () {
            return this.replace(/^\s*/, "").replace(/\s*$/, "");
        };

        $('[readonly]').focus(function () { // delete cursor for readonly fields
            $('[readonly]').blur();
        });

        let lines = new Lines();
        $('.indexed-line:has([readonly]):last').filter((index, line) => { // deleting empty line for readonly cases
            return lines.line_is_empty($(line));
        }).remove();

        lines.clone_last_line($("form"));

        if (validate === "True") {
            $('.indexed-line').removeClass('indexed-line')
        }
        document.addEventListener('mouseup', PopUp.hideOnMouseUp);
        if (view === "True" || validate === "True") {
            console.log('ads');
            document.querySelectorAll(".popup-comment-content > textarea").forEach(Cell.markCommented)
        }

        $(".table-comment-wrapper").on('shown.bs.collapse', Comment.focus);

        $("#sync").show();

        document.onkeydown = onKeyDownAction;

        window.addEventListener("beforeunload", function (e) {
            Journal.send_all_forms();
        }, false);
    }
}
class Comment {

    static add(textarea) {
        _.debounce((textarea) => {
            let forSend = JSON.stringify({
                "cell_location": {
                    "field_name": $(textarea).parent().siblings("input").name,
                    "table_name": $(textarea).parent().siblings("input").attr("table-name"),
                    "group_id": $(textarea).parent().siblings("input").attr("journal-page"),
                    "index": $(textarea).parent().siblings("input").attr("index")
                },

                "message": {
                    "text": $(textarea).val(),
                    "link": Cell.getLink($(textarea).parent().siblings("input")),
                    "type": "comment",
                },
            });
            $.ajax({
                url: "/common/messages/add_comment/",
                type: "POST",
                contentType: "application/json; charset=utf-8",
                data: forSend,
                success: function (json) {
                    if (json && json.result) {
                        // console.log(json.result)
                    }
                }
            });
        }, 300)(textarea);
    }

    static collapse(element) {

        let container = $(element).parent().find(".comment__text");
        container.collapse('toggle');
    }

    static focus(event) {
        $(event.target).children(".table-comment").focus();
    }

}
