import formulaParser from 'hot-formula-parser'
import store from '../../store/store'
var FormulaParser = require('hot-formula-parser').Parser;
var request = require('sync-request');

function isNumeric(num) {
    return !isNaN(num)
}

if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match;
        });
    };
}

console.log("Loading formula...")
var parser = new FormulaParser();
window.parser = parser
window.parser.setFunction('FUNC', function(params) {
    try {
        const journal = params[0];
        const table = params[1];
        const field = params[2];
        const index = params[3];
        var shift_delta = params[4];
        try {
            shift_delta = -Number(shift_delta)
        }
        catch(e) {
            console.log(e)
        }

        var shifts = store.getters['journalState/events']
        const current_journal = store.getters['journalState/journalName']
        const current_shift = store.getters['journalState/journalInfo'].id
        const current_shift_start_time = store.getters['journalState/journalInfo'].start_time
        let res = 0;
        let result = null
        if (journal == current_journal && shift_delta == 0) {
            let formula = store.getters['journalState/fieldFormula'](table, field)
            if (formula) {
                result =  window.parser.parse(formula)
            } else {
                result = store.getters['journalState/cell'](table, field, index)['value']
            }
        } else {
            for (var i in shifts) {
                if (shifts[i].start == current_shift_start_time) {
                    var index = i;
                }
            }
            var shift = shifts[(index - shift_delta) % shifts.length].url.split("/")[3]
            res = request("GET", window.HOSTNAME + "/api/cell/?journal={0}&table={1}&field={2}&shift={3}".format(journal, table, field, shift))
            let json = JSON.parse(res.getBody())
            console.log(json)
            if (json.value == null) {
                result = undefined
            }
            else if (isNumeric(json.value)) {
                result = Number(json.value)
            }
            else {
                result = window.parser.parse(json.value).result
            }
        }
        return result
    }
    catch(e){
        console.log(e)
    }
})

var getCellFromVariable = function(variable) {
    var params = variable.split("(")[1].replace(/(\s)|(")|(\))/g, "").split(",")
    const journal = params[0];
    const table = params[1];
    const field = params[2];
    const index = params[3];
    const shift = params[4];
    return {journal: journal, table: table, field: field, index: index, shift: shift}
}

var getCellsFromFormula = function(formula) {
    var re = /FUNC\([^\)]*\)/g;
    var variables = [];
    do {
        m = re.exec(formula);
        if (m) {
            variables.push(m);
        }
    } while (m);
    return variables.map(getCellFromVariable)
}

var getCellValue = function(cell) {
    var res = request("GET", window.HOSTNAME + "/api/cell/?journal={0}&table={1}&field={2}&shift={3}".format(cell.journal, cell.table, cell.field, cell.shift))
    let json = JSON.parse(res.getBody())
    return json.value
}

function isEquivalent(a, b) {
    // Create arrays of property names
    var aProps = Object.getOwnPropertyNames(a);
    var bProps = Object.getOwnPropertyNames(b);

    // If number of properties is different,
    // objects are not equivalent
    if (aProps.length != bProps.length) {
        return false;
    }

    for (var i = 0; i < aProps.length; i++) {
        var propName = aProps[i];

        // If values of same property are not equal,
        // objects are not equivalent
        if (a[propName] !== b[propName]) {
            return false;
        }
    }

    // If we made it this far, objects
    // are considered equivalent
    return true;
}

function containsObject(obj, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (isEquivalent(list[i], obj)) {
            return true;
        }
    }

    return false;
}

// true when formula creates cycle
function checkFormula(formula, cell) {
    var cells = getCellsFromFormula(formula)
    if (containsObject(cell, cells)) {
        return true
    } else {
        values = variables.map(getCellValue)
        results = []
        for (var value in values) {
            if (!isNumeric(value)) {
                results.push(checkFormula(value, cell))
            } else {
                results.push(false)
            }
        }
        let sum = results.reduce((a, b) => {
            return a + b
        }, 0)
        if (sum > 0) {
            return true
        } else {
            return false
        }
    }

}
