import $ from 'jquery'
import _ from 'lodash'

    /**
 * @return {boolean}
 */function IsJsonString(str) {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    }

const CELL_CLASS = "general-value";

class Cell {
    constructor() {

    }

    // public
    static onInput(input) {
        console.log('onInput', input.value)
        this.on_input_change(input);
        this.saveCell(input);
        $('#sync').hide();$('#async').show();
    }

    static onChange(input) {
        console.log('onChange', input.value)
        this.reformat_on_change(input);
        this.addMessage(input);
    }

    //private
    static saveCell(input) {
        let forSend = JSON.stringify({
            'cell_location': {
                'field_name': input.name,
                'table_name': $(input).attr('table-name'),
                'group_id': $(input).attr('journal-page'),
                'index': $(input).attr('index')
            },
            'value': input.value,
        });
        $.ajax({
            url: "/common/save_cell/",
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: forSend,
            success: function (json) {
                if (json && json.status) {
                    $('#async').hide();
                    $('#sync').show();
                }
            }
        });
    }
    static saveComment(cell) {

        _.debounce((cell) => {
            console.info(cell);
            let forSend = JSON.stringify({
                'cell_location': {
                    'field_name': cell.name,
                    'table_name': cell.getAttribute('table-name'),
                    'group_id': cell.getAttribute('journal-page'),
                    'index': cell.getAttribute('index')
                },
                'message': {
                    'text': cell.getAttribute('comment'),
                    'link': Cell.getLink(cell),
                    'type': 'comment'
                },
                "crud":"add",
            });
            // $.ajax({
            //     url: "/common/messages/add_comment/",
            //     type: 'POST',
            //     contentType: 'application/json; charset=utf-8',
            //     data: forSend,
            //     success: function (json) {
            //         if (json && json.result) {
            //              console.log(json.result)
            //         }
            //     }
            // });
            messages_socket.send(forSend);
        }, 300)(cell);
    }


    /**
     *
     * @param cell instance in DOM
     */


    static addMessage(msg) {
        let debounce = _.debounce((input) => {

            const json = input.dataset.info.replace(/'/g, '"');
            const info = JSON.parse(json);

            if (input.type === "number" && (input.value * 1 < info.min_normal || input.value * 1 > info.max_normal) && input.value != '') {
                let forSend = JSON.stringify({
                    'cell': {
                        'field_name': input.name,
                        'table_name': $(input).attr('table-name'),
                        'group_id': $(input).attr('journal-page'),
                        'index': $(input).attr('index')
                    },
                    'crud': "add",
                    'message': {
                        'text': input.value,
                        'link': Cell.getLink(input),
                        'type': 'critical_value'
                    },
                });
                // $.ajax({
                //     url: "/common/messages/add_critical/",
                //     type: 'POST',
                //     contentType: 'application/json; charset=utf-8',
                //     data: forSend,
                //     success: function (json) {
                //         if (json && json.status) {
                //             // console.log(json.result)
                //         }
                //     }
                // });
                messages_socket.send(forSend);
            } else {

                let forSend = JSON.stringify({
                    'cell': {
                        'field_name': input.name,
                        'table_name': $(input).attr('table-name'),
                        'group_id': $(input).attr('journal-page'),
                        'index': $(input).attr('index')
                    },
                    "crud":"update",
                });

                // $.ajax({
                //     url: "/common/messages/update/",
                //     type: 'POST',
                //     contentType: 'application/json; charset=utf-8',
                //     data: forSend,
                //     success: function (json) {
                //         if (json && json.status) {
                //             // console.log(json.result)
                //         }
                //     }
                // });
                messages_socket.send(forSend);
            }
        },
            300);

        debounce(msg)
    }



    static on_input_change(input) {
        console.log(input.dataset.info);

        if (input.dataset.info === 'undefined') return;

        const json = input.dataset.info.replace(/'/g, '"');
        // if field description exists
        let info = null;
        if (IsJsonString(json)) {
           info = JSON.parse(json);

        }else{
          // default field description
           info = {'type': 'text'};
        }
        input.type = info.type;
        if (input.type === "number") {
            if ((input.value * 1 < info.min_normal || input.value * 1 > info.max_normal) && input.value != '') {
                $(input).css('color', 'red');
            } else {
                $(input).css('color', 'black');
            }


            console.log(input.value);


        } else if (info.type === "datalist") {
            if ($(input).attr('data-pagmode') === "validate") {
                $(input).removeAttr("type");
            } else {

                $(input).removeAttr("type");
                $(input).attr('list', 'datalist');

                if ($('#datalist').length === 0) {
                    $(input).after('<datalist id="datalist"></datalist>');
                    info.options.forEach((name) => {
                        $("#datalist").append("<option>" + name + "</option>");
                    })
                }
            }
        }

        $(input).attr('placeholder', info.units);
        this.markCommented(input);
    }


    static getLink(input) {
        let plant = location.pathname.split('/')[1];
        let journal_name = location.pathname.split('/')[2];
        let journal_id = location.search.split("?")[1].split("id=")[1]
        let result = `/${plant}/${journal_name}?id=${journal_id}&page_mode=view&highlight=${$(input).attr("id")}#${$(input).attr("id")}`;

        return result;
    }

    static reformat_on_change(input) {
        if (input.value === "") {
            input.value = 0
        }
        if (input.type === "number") {
            input.value = +(input.value*1.0).toFixed(2)
        }
        // $(input.closest('table')).alignColumn([1, 2, 3, 4, 5], {center: '.'})
    }

    static markCommented(textarea) {
        let comment = $(textarea).parent()[0];
        let comment_notification = $(comment).siblings("i")[0];
        if ($(textarea).val()) {
            $(comment_notification).addClass("show")
        }
        else {
            $(comment_notification).removeClass("show")
        }
    }

    static resize_cell(input) {
        input.style.width = (input.value.length + 1) + 'ch';
    }
}


$(document).ready(() => {
   window.Cell = Cell;
});


export {IsJsonString, Cell};
