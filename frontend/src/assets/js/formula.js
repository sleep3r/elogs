import formulaParser from 'hot-formula-parser'
import store from '../../store/store'
import ajax from '../../axios.config'
var FormulaParser = require('hot-formula-parser').Parser;


function isNumeric(num) {
    return !isNaN(num)
}

if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined' ?
                args[number] :
                match;
        });
    };
}

console.log("Loading formula...");
var parser = new FormulaParser();
window.parser = parser;


export function getValue(params) {
    try {
        var params_num = this.isTableIndexed ? 5 : 4;
        while (params.length < params_num) {
            params.splice(0, 0, false)
        }
        const journal = params[0] ? params[0] : this.journal;
        var shift_delta = params[1] ? params[1] : this.shift;
        const table = params[2] ? params[2] : this.table;
        const field = params[3] ? params[3] : this.field;
        const index = this.isTableIndexed ? 0 : params[4] ? params[4] : this.index;

        shift_delta = -Number(shift_delta);
        var shifts = store.getters['formulaState/shifts']();
        const current_journal = store.getters['journalState/journalName'];
        const current_shift_start_time = store.getters['journalState/journalInfo'].start_time;
        let res = 0;
        let result = null;
        if (journal == current_journal && shift_delta == 0) {
            let formula = store.getters['journalState/fieldFormula'](table, field);
            if (formula) {
                result = window.parser.parse(formula)
            } else {
                result = store.getters['journalState/cell'](table, field, index)['value']
            }
        } else {
            let shift_index;
            for (var i in shifts) {
                if (shifts[i].start == current_shift_start_time) {
                    shift_index = i;
                }
            }
            let shift = shifts[(shift_index - shift_delta) % shifts.length].id;
            let formula = store.getters['formulaState/fieldFormula'](journal, shift, table, field);
            let value = store.getters['formulaState/fieldValue'](journal, shift, table, field, index);
            if (formula) {
                window.parser.setFunction("FUNC", getValue.bind({
                    journal: state.journalInfo.journal.name,
                    table: table,
                    field: field,
                    index: index,
                    shift: shift,
                    isTableIndexed: false,
                }));
                result = window.parser.parse(formula)
            }
            // value === undefined – value have not been downloaded
            // value === null – value downloaded and is null
            // value === str - true value
            else if (value !== undefined) {
                result = value;
            } else {
                ajax.get(window.HOSTNAME + "/api/cell/",
                    {
                        params: {
                            journal: journal,
                            table: table,
                            field: field,
                            shift: shift,
                        }
                    })
                    .then(response => {
                        let value = response.data.value;
                        let formula = response.data.formula;
                        store.commit('formulaState/ADD_CELL', {
                            journalName: journal,
                            tableName: table,
                            fieldName: field,
                            shiftNum: shift,
                            value: value,
                            formula: formula,
                        })
                    })
            }
        }
        return result;
    } catch (e) {
        console.log(e);
    }
}

