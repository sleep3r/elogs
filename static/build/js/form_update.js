/*jshint esversion: 6 */
"use strict";


function shift_confirmation() {
    let edit = $("input[name='edit']").attr("value");
    if (edit === "True") {
        let has_edited = $("input[name='has_edited']").attr("value");
        console.log(has_edited);
        if (!(has_edited === "True")) {
            $.confirm({
                title: 'Продолжить?',
                content: 'Вы будете назначены отвественным за этот журнал',
                autoClose: 'cancel|60000',
                theme: 'supervan',
                buttons: {
                    confirm: {
                        text: "Да",
                        action: function() {$("form").trigger("input")}
                    },
                    cancel: {
                        text: "Назад",
                        action: function () {
                            history.back();
                        },
                    }
                }
            });
        }
    }
}



/**
 * @dependecies Journal
 * @param e
 */
var selectedElement = null;

function onKeyDownAction(e) {
    // if 'input' is active(e.g page mode is 'edit')
    if (document.activeElement.tagName === 'INPUT') {
        let input = document.activeElement;
        if (input.type === 'number') {
            var popup = input.parentElement.getElementsByClassName('input-check-popup')[0];
            // If number or ',' or '.' was pressed
            if ((e.keyCode >= 48 && e.keyCode <= 57) || e.keyCode == '188' || e.keyCode == '190') {
                console.log('number was pressed in number field');
                popup.classList.remove('show')
            } else {
                if (e.keyCode != '8' &&
                    e.keyCode != '46' &&
                    e.keyCode != '37' &&
                    e.keyCode != '38' &&
                    e.keyCode != '39' &&
                    e.keyCode != '40') {
                    popup.classList.add('show');
                    setTimeout(function () {
                        popup.classList.remove('show');
                    }, 1500);
                    console.log('not number was pressed in number field')
                }
                else {
                    popup.classList.remove('show');
                }
                // backspace and delete
                if (e.keyCode != '8' && e.keyCode != '46') {
                    e.preventDefault();
                }
            }
        }
        selectedElement = input.parentElement;
    }

    // if 'span' is active(e.g page mode is 'validate')
    if (document.activeElement.tagName === 'TEXTAREA') {
        this.start = document.activeElement.parentElement.parentElement;
    }
    e = e || window.event;

    if (e.keyCode == '38') { // up arrow
        var idx = selectedElement.cellIndex;
        var nextrow = selectedElement.parentElement.previousElementSibling;
        if (nextrow != null) {
            var sibling = nextrow.cells[idx];
            if (sibling) {
                Journal.focusTo(sibling);
            }
        }
    } else if (e.keyCode == '40') { // down arrow
        var idx = selectedElement.cellIndex;
        var nextrow = selectedElement.parentElement.nextElementSibling;
        if (nextrow != null) {
            var sibling = nextrow.cells[idx];
            if (sibling) {
                Journal.focusTo(sibling);
            }
        }
    } else if (e.keyCode == '37') { // left arrow
        var sibling = selectedElement.previousElementSibling;
        if (sibling) {
            Journal.focusTo(sibling);
        }
    } else if (e.keyCode == '39') { // right arrow
        var sibling = selectedElement.nextElementSibling;
        if (sibling) {
            Journal.focusTo(sibling);
        }
    }
}


$(document).ready(function () {
    shift_confirmation();
    Journal.onReady();
});



