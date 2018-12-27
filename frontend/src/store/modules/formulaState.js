import ajax from '../../axios.config'
import VueCookies from 'vue-cookies'
import {getValue} from '../../assets/js/formula'
import Vue from 'vue';
import _ from 'lodash';
var FormulaParser = require('hot-formula-parser').Parser;


const formulaState = {
    namespaced: true,
    state: {
        journalsInfo: {},
    },
    getters: {
        cell: (state) => (journalName, shiftNum, tableName, fieldName, rowIndex) => {
            let journal = state.journalsInfo[journalName] ? state.journalsInfo[journalName] : {};
            let table = journal[tableName] ? journal[tableName] : {};
            let field = table[fieldName]? table[fieldName] : {};
            return {
                value: field[rowIndex]
            };
            if (!(field)) {
                // console.log('WARNING! Trying to get cell value of unexistent field: ' + fieldName);
                return {};
            }
            if (field.formula) {
                setTimeout(window.parser.setFunction("FUNC", getValue.bind({
                    journal: state.journalInfo.journal.name,
                    table: tableName,
                    field: fieldName,
                    index: rowIndex,
                    shift: 0,
                    isTableIndexed: false,
                })), 0) // Timout for sequential functions execution
                return {
                    value: window.parser.parse(field.formula).result
                };
            }

            let cells = field.cells;
            if (Object.keys(cells).length !== 0) {
                if (rowIndex in cells) {
                    return cells[rowIndex];
                }
                else {
                    // console.log('WARNING! Trying to get cell value with unexistent index: ' + fieldName + ' ' + rowIndex);
                    return {};
                }
            }
            else {
                return {};
            }
        },
        fieldFormula: (state) => (journalName, shiftNum, tableName, fieldName) => {
            console.log(journalName)
            console.log(state.journalsInfo[journalName])
            let journal = state.journalsInfo[journalName] ? state.journalInfo[journalName] : {};
            let shift =  journal[shiftNum] ? journal[shiftNum] : {};
            let table = shift[tableName] ? shift[tableName] : {};
            let field = table[fieldName] ? table[fieldName] : {};
            return field.formula || '';
        },
    },
    mutations: {
        ADD_CELL (state, payload) {
            console.log(payload)
            console.log("formulaState/mutations/ADD_CELL");
            journalName = payload.journalName
            shiftNum = payload.shiftNum
            tableName = payload.tableName
            fieldName = payload.fieldName
            let journal = state.journalsInfo[journalName] ? state.journalInfo[journalName] : {};
            if (_.isEmpty(journal)) {
                Vue.set(state.journalsInfo, payload.journalName, {})
            }
            let shift =  journal[shiftNum] ? journal[shiftNum] : {};
            if (_.isEmpty(shift)) {
                Vue.set(state.journalInfo[journalName], shiftNum, {})
            }
            let table = shift[tableName] ? shift[tableName] : {};
            if (_.isEmpty(table)) {
                Vue.set(state.journalInfo[journalName][shiftNum], tablelName, {})
            }
            let field = table[fieldName]
            if (!field) {
                Vue.set(
                    state.journalInfo[payload.journalName][payload.tableName], 
                    payload.fieldName, 
                    payload.value
                )
            }
        },
    }
}

export default formulaState