import axios from 'axios';

const journalState = {
    namespaced: true,
    state: {
        journalInfo: {},
        loaded: false,
    },
    getters: {
        loaded: state => state.loaded,
        tables: state => {
            if (state.loaded) {
                return Object.keys(state.journalInfo.journal.tables);
            } else {
                return [];
            }
        },
        plantName: state => {
            if (state.loaded) {
                return state.journalInfo.plant.name;
            } else {
                return '';
            }
        },
        journalName: state => {
            if (state.loaded) {
                return state.journalInfo.journal.name;
            } else {
                return '';
            }
        },
        shiftOrder: state => {
            if (state.loaded) {
                return state.journalInfo.order
            } else {
                return -1;
            }
        },
        cellValue: (state) => (tableName, fieldName, rowIndex) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                if (!(fieldName in fields)) {
                    console.log('WARNING! Trying to get cell value of unexistent field: ' + fieldName);
                    return '';
                }
                let cells = fields[fieldName].cells;
                if (Object.keys(cells).length !== 0) {
                    if (rowIndex in cells) {
                        return cells[rowIndex].value;
                    }
                }
                else {
                    return '';
                }
            }
        },
        maxRowIndex: (state) => (tableName) => {
            if (state.loaded) {
                let max = -1;
                let fields = state.journalInfo.journal.tables[tableName].fields;
                for(let field in fields) {
                    for (let index in fields[field].cells) {
                        index = parseInt(index);
                        max = max < index ? index : max;
                    }
                }
                return max+1;
            } else {
                return -1;
            }
        },
        tableTitle: (state) => (tableName) => {
            return 'Заголовок таблицы'
        },
        fieldDescription: (state) => (tableName, fieldName) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                if (!(fieldName in fields)) {
                    console.log("WARNING! Trying to get field desctiption of unexistent field: " + fieldName);
                    return {};
                }
                return fields[fieldName].field_description || ''
            }
            else {
                return ''
            }
        }
    },
    mutations: {
        UPDATE_JOURNAL_INFO (state, journalInfo) {
            state.journalInfo = journalInfo;
        },
        SET_LOADED (state, loaded) {
            state.loaded = loaded;
        },
        SAVE_CELL_VALUE (state, payload) {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[payload.tableName].fields;
                if (!(payload.fieldName in fields)) {
                    console.log('WARNING! Trying to save value of unexistent field: ' + payload.fieldName);
                    console.log('  Creating field ' + payload.fieldName + '...');
                    fields[payload.fieldName] = {};
                    fields[payload.fieldName]['cells'] = {};
                }
                let cells = fields[payload.fieldName].cells;
                if (payload.index in cells) {
                    // update cell
                    cells[payload.index]['value'] = payload.value;
                }
                else {
                    // create cell
                    cells[payload.index] = {};
                    cells[payload.index]['value'] = payload.value;
                }
            }
        }
    },
    actions: {
        loadJournal: function ({ commit, state, getters }, payload) {
            axios
                .get('http://localhost:8000/api/shifts/' + payload)
                .then(response => {
                    commit('UPDATE_JOURNAL_INFO', response.data);
                    commit('SET_LOADED', true);
                })
        },
    }
}

export default journalState