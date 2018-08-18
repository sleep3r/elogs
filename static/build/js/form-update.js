import {Cell} from './cell'

/*jshint esversion: 6 */
"use strict";

/**
 * @dependecies Journal, CELL_CLASS
 * @param e
 */
var selectedElement = null;

function onKeyDownAction(e) {

    if (document.activeElement.tagName === 'INPUT') {
        const input = document.activeElement;
        selectedElement = input.parentElement;
    }

    // if 'span' is active(e.g page mode is 'validate')
    if (document.activeElement.tagName === 'TEXTAREA') {
        this.start = document.activeElement.parentElement.parentElement;
    }
    e = e || window.event;

    if (e.keyCode === 38) { // up arrow
        let idx = selectedElement.cellIndex;
        let nextrow = selectedElement.parentElement.previousElementSibling;
        if (nextrow != null) {
            let sibling = nextrow.cells[idx];
            if (sibling) {
                Journal.focusTo(sibling);
            }
        }
    } else if (e.keyCode === 40) { // down arrow
        let idx = selectedElement.cellIndex;
        let nextrow = selectedElement.parentElement.nextElementSibling;
        if (nextrow != null) {
            let sibling = nextrow.cells[idx];
            if (sibling) {
                Journal.focusTo(sibling);
            }
        }
    } else if (e.keyCode === 37) { // left arrow
        let sibling = selectedElement.previousElementSibling;
        if (sibling) {
            Journal.focusTo(sibling);
        }
    } else if (e.keyCode === 39) { // right arrow
        let sibling = selectedElement.nextElementSibling;
        if (sibling) {
            Journal.focusTo(sibling);
        }
    }
}


$(document).ready(function () {
    Shift.confirm();
    Journal.onReady();
});
