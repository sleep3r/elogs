class FormTable {

    constructor() {

    }

    static on_form_change(form) {
        let lines = new Lines();
        lines.clone_last_line(form);
        lines.clear_empty_lines(form);
        FormTable.send(form);
    }

    static send(form) {
        _.debounce((form) => {
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
        }, 300)(form);
    }

}


class Lines {

    constructor() {

    }

    line_is_empty(tr_line) {
        let filled = 0;
        tr_line.find('input.general-value').each(function () {
            if (this.value.trim() !== "") {
                filled++;
            }
        });

        return filled === 0;
    }

    clone_last_line(form) {
        const tables = $(form).find("table:not(.table-insided)");
        for (let i=0; i<tables.get().length; i++) {
            let table = $(tables.get()[i]);
            const last_line = table.find(".indexed-line:last");
            if (!this.line_is_empty(last_line)) {
                let new_last_line = last_line.clone();
                new_last_line.find("input").val("");
                new_last_line.find("textarea").val("");
                new_last_line.find("input").attr('index', last_line.find("input").attr('index')*1 + 1);
                new_last_line.find("input").attr('id', last_line.find("input").attr('id').replace(/(-\d+)+/g, function(match, number) {
                    return parseInt(number)-1}));
                new_last_line.find(".index-input").val(last_line.find(".index-input").val() * 1 + 1);
                table.append(new_last_line);
            }
        }
    }


    clear_empty_lines(form) {
        const tables = $(form).find("table:not(.table-insided)");
        let context = this;
        for (let i=0; i<tables.get().length; i++) {
            let table = $(tables.get()[i]);
            let last_line = null;

            $(table.find(".indexed-line").get().reverse()).each(function (index) {
                if (context.line_is_empty($(this))) {
                    if (last_line) {
                        last_line.remove();
                    }
                    last_line = this;
                } else {
                    return false;
                }
            });
        }
    }

}
