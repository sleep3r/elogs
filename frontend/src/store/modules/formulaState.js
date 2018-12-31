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
        shifts: [],
    },
    getters: {
        shifts: (state) => () => {
            return state.shifts;
        },
        cell: (state) => (journalName, shiftNum, tableName, fieldName, rowIndex) => {
            let journal = state.journalsInfo[journalName] ? state.journalsInfo[journalName] : {};
            let shift = journal[shiftNum] ? journal[shiftNum] : {}
            let table = shift[tableName] ? shift[tableName] : {};
            let field = table[fieldName];
            console.log(journal, shift, table, field);
            return {
                value: field
            };
        },
        fieldFormula: (state) => (journalName, shiftNum, tableName, fieldName) => {
            console.log(journalName)
            console.log(state.journalsInfo[journalName])
            let journal = state.journalsInfo[journalName] ? state.journalsInfo[journalName] : {};
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
            let journalName = payload.journalName
            let shiftNum = payload.shiftNum
            let tableName = payload.tableName
            let fieldName = payload.fieldName
            let journal = state.journalsInfo[journalName] ? state.journalsInfo[journalName] : {};
            if (_.isEmpty(journal)) {
                Vue.set(state.journalsInfo, payload.journalName, {})
            }
            let shift =  journal[shiftNum] ? journal[shiftNum] : {};
            if (_.isEmpty(shift)) {
                Vue.set(state.journalsInfo[journalName], shiftNum, {})
            }
            let table = shift[tableName] ? shift[tableName] : {};
            if (_.isEmpty(table)) {
                Vue.set(state.journalsInfo[journalName][shiftNum], tableName, {})
            }
            let field = table[fieldName]
            if (!field) {
                Vue.set(
                    state.journalsInfo[payload.journalName][shiftNum][payload.tableName], 
                    payload.fieldName, 
                    payload.value
                )
            }
        },
        ADD_SHIFTS (state, payload) {
            state.shifts = payload
        }
    },
    actions: {
        loadLastShifts: function ({ commit, state, getters }, payload) {
            ajax.get(
                window.HOSTNAME+`/api/last_shifts/?plant=${payload.plantName}&journal=${payload.journalName}`
            )
            .then(response => {
                commit('ADD_SHIFTS', response.data)
            });
        }
    }
}

export default formulaState