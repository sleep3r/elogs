import { Shift } from "../../assets/js/shift";
import {Journal} from "./journal";

import $ from 'jquery'
// import './journal'

/*jshint esversion: 6 */
"use strict";

/**
 * @dependecies Journal
 * @param e
 */
let selectedElement = null;

function onKeyDownAction(e) {
    // if 'input' is active(e.g page mode is 'edit')
    if (document.activeElement.tagName === 'INPUT') {
        const input = document.activeElement;
        if (input.type === 'number') {
            const popup = input.parentElement.getElementsByClassName('input-check-popup')[0];
            // If number or ',' or '.' was pressed
            console.log('key pressed:', e.keyCode);
            if ((e.keyCode >= 48 && e.keyCode <= 57) || e.keyCode === 188 || e.keyCode === 190) {
                console.log('number was pressed in number field');
                popup.classList.remove('show')
            } else {
                if (e.keyCode !== 8 &&
                    e.keyCode !== 46 &&
                    e.keyCode !== 37 &&
                    e.keyCode !== 38 &&
                    e.keyCode !== 39 &&
                    e.keyCode !== 40) {
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
                if (e.keyCode !== 8 && e.keyCode !== 46) {
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
    window.onKeyDownAction = onKeyDownAction;
    Shift.confirm();
    Journal.onReady();
});


export {onKeyDownAction};


