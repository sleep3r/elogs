import axios from 'axios';
import VueCookies from 'vue-cookies'

const journalState = {
    namespaced: true,
    state: {
        plantsInfo: [],
        journalInfo: {},
        events: [],
        loaded: false,
        socket: {
            isConnected: false,
            reconnectError: false,
        },
        isSynchronized: true
    },
    getters: {
        loaded: state => state.loaded,
        journalInfo: state =>  state.journalInfo,
        events: state =>  state.events,
        tables: state => {
            if (state.loaded) {
                return Object.keys(state.journalInfo.journal.tables);
            } else {
                return [];
            }
        },
        isSynchronized: state => state.isSynchronized,
        plants: state => {
            return state.plantsInfo
        },
        plantName: state => {
            if (state.loaded) {
                return state.journalInfo.plant.name;
            } else {
                return '';
            }
        },
        plantVerboseName: state => {
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
        journalVerboseName: state => {
            if (state.loaded) {
                return state.journalInfo.journal.name;
            } else {
                return '';
            }
        },
        tableVerboseName: (state) => (tableName) => {
            if (state.loaded) {
                return tableName;
            } else {
                return '';
            }
        },
        fieldVerboseName: (state) => (tableName, fieldName) => {
            if (state.loaded) {
                return fieldName;
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
                    // console.log('WARNING! Trying to get cell value of unexistent field: ' + fieldName);
                    return '';
                }
                let cells = fields[fieldName].cells;
                if (Object.keys(cells).length !== 0) {
                    if (rowIndex in cells) {
                        return cells[rowIndex].value;
                    }
                    else {
                        // console.log('WARNING! Trying to get cell value with unexistent index: ' + fieldName + ' ' + rowIndex);
                        return '';
                    }
                }
                else {
                    return '';
                }
            }
        },
        cellComment: (state) => (tableName, fieldName, rowIndex) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                if (!(fieldName in fields)) {
                    // console.log('WARNING! Trying to get cell comment of unexistent field: ' + fieldName);
                    return '';
                }
                let cells = fields[fieldName].cells;
                if (Object.keys(cells).length !== 0) {
                    if (rowIndex in cells) {
                        return cells[rowIndex].comment;
                    }
                    else {
                        // console.log('WARNING! Trying to get cell comment with unexistent index: ' + fieldName + ' ' + rowIndex);
                        return '';
                    }
                }
                else {
                    return '';
                }
            }
        },
        fieldCells: (state) => (tableName, fieldName) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                if (fieldName in fields) {
                    return state.journalInfo.journal.tables[tableName].fields[fieldName].cells
                }
                else return []
            } else {
                return []
            }
        },
        unsyncJournalCells: (state, getters) => () => {
            let unsyncCells = []
            getters.tables.map((table, index) => {
                let currentTable = state.journalInfo.journal.tables[table]
                for (let field in currentTable.fields) {
                    let currentCells = currentTable.fields[field].cells
                    for (let cell in currentCells) {
                        if (currentCells[cell].notSynchronized) {
                            unsyncCells.push(currentCells[cell])
                        }
                    }
                }
            })
            return unsyncCells
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
        rowIsEmpty: (state) => (tableName, index) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields
                for (let field in fields) {
                    if ('cells' in fields[field]) {
                        if (index in fields[field].cells) {
                            return false
                        }
                    }
                }
                return true
            }
        },
        tableTitle: (state) => (tableName) => {
            return 'Заголовок таблицы'
        },
        fieldDescription: (state) => (tableName, fieldName) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                if (!(fieldName in fields)) {
                    // console.log("WARNING! Trying to get field desctiption of unexistent field: " + fieldName);
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
        SET_SYNCHRONIZED (state, isSynchronized) {
            state.isSynchronized = isSynchronized
        },
        UPDATE_JOURNAL_INFO (state, journalInfo) {
            state.journalInfo = journalInfo;
        },
        UPDATE_PLANTS_INFO (state, plantsInfo) {
            state.plantsInfo = plantsInfo;
        },
        SET_LOADED (state, loaded) {
            state.loaded = loaded;
        },
        SAVE_CELL_VALUE (state, payload) {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[payload.tableName].fields;
                if (!(payload.fieldName in fields)) {
                    // console.log('WARNING! Trying to save value of unexistent field: ' + payload.fieldName);
                    // console.log('  Creating field ' + payload.fieldName + '...');
                    fields[payload.fieldName] = {};
                    fields[payload.fieldName]['cells'] = {};
                }
                let cells = fields[payload.fieldName].cells;
                if (payload.value) {
                    if (payload.index in cells) {
                        // update cell
                        cells[payload.index]['value'] = payload.value;
                        if (payload.notSynchronized) {
                            cells[payload.index]['notSynchronized'] = payload.notSynchronized;
                            cells[payload.index]['fieldName'] = payload.fieldName;
                            cells[payload.index]['tableName'] = payload.tableName;
                            cells[payload.index]['index'] = payload.index;
                        }
                    }
                    else {
                        // create cell
                        Vue.set(cells, payload.index, {});
                        Vue.set(cells[payload.index], 'value', payload.value);
                        if (payload.notSynchronized) {
                            Vue.set(cells[payload.index], 'notSynchronized', payload.notSynchronized);
                        }
                    }
                }
                else {
                    Vue.delete(cells, payload.index);
                }
            }
        },
        SAVE_CELL_COMMENT (state, payload) {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[payload.tableName].fields;
                if (!(payload.fieldName in fields)) {
                    // console.log('WARNING! Trying to save comment of unexistent field: ' + payload.fieldName);
                    // console.log('  Creating field ' + payload.fieldName + '...');
                    fields[payload.fieldName] = {};
                    fields[payload.fieldName]['cells'] = {};
                }
                let cells = fields[payload.fieldName].cells;
                if (payload.comment) {
                    if (payload.index in cells) {
                        // update cell
                        Vue.set(cells[payload.index], 'comment', payload.comment);
                    }
                    else {
                        // create cell
                        Vue.set(cells, payload.index, {});
                        Vue.set(cells[payload.index], 'comment', payload.comment);
                    }
                }
                else {
                    Vue.delete(cells, payload.index);
                }
            }
        },
        SET_PAGE_MODE (state, mode) {
            if (state.loaded) {
                state.journalInfo.mode = mode
            }
        },
        DELETE_TABLE_ROW (state, payload) {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[payload.tableName].fields;
                for (let field in fields) {
                    if ('cells' in fields[field]) {
                        let cells = fields[field]['cells']
                        for (let i=0; i<=payload.maxRowIndex; i++) {
                            if (i == payload.index) {
                                Vue.delete(cells, i);
                            }
                            if (i > payload.index) {
                                if (cells[i]) {
                                    Vue.set(cells, i-1, cells[i]);
                                    Vue.delete(cells, i);
                                }
                            }
                        }
                    }
                }
            }
        },
        INSERT_EMPTY_TABLE_ROW (state, payload) {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[payload.tableName].fields;
                for (let field in fields) {
                    if ('cells' in fields[field]) {
                        let cells = fields[field]['cells']
                        for (let i=payload.maxRowIndex; i>=0; i--) {
                            if (i >= payload.index) {
                                if (cells[i]) {
                                    Vue.set(cells, i+1, cells[i]);
                                    Vue.delete(cells, i)
                                }
                            }
                            if (i == payload.index) {
                                Vue.set(cells, i, '')
                            }
                        }
                    }
                }
            }
        },
        FLUSH_TABLE_ROW (state, payload) {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[payload.tableName].fields;
                for (let field in fields) {
                    if ('cells' in fields[field]) {
                        let cells = fields[field]['cells']
                        for (let i=payload.maxRowIndex; i>=0; i--) {
                            if (i == payload.index) {
                                Vue.set(cells, i, '')
                            }
                        }
                    }
                }
            }
        },
        SOCKET_ONOPEN (state, event)  {
            Vue.prototype.$socket = event.currentTarget
            state.socket.isConnected = true
        },
        SOCKET_ONCLOSE (state, event)  {
            state.socket.isConnected = false
        },
        SOCKET_ONERROR (state, event)  {
            console.error(state, event)
        },
        SOCKET_ONMESSAGE (state, message)  {

        },
        SOCKET_RECONNECT(state, count) {
            console.info(state, count)
        },
        SOCKET_RECONNECT_ERROR(state) {
            state.socket.reconnectError = true;
        },
    },
    actions: {
        loadJournal: function ({ commit, state, getters }, payload) {
            let id = payload['id'] ? payload['id'] : ''
            return axios
                .get('http://localhost:8000/api/shifts/' + id, {
                    withCredentials: true,
                    params: {
                        'plantName': payload['plantName'],
                        'journalName': payload['journalName']
                    }
                })
                .then(response => {
                    commit('UPDATE_JOURNAL_INFO', getters.isSynchronized ? response.data : JSON.parse(localStorage.getItem('vuex')).journalState.journalInfo);
                    commit('SET_LOADED', true);
                    return response.data.id
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        loadPlants: function ({ commit, state, getters }) {
            axios
                .get('http://localhost:8000/api/menu_info/')
                .then(response => {
                    commit('UPDATE_PLANTS_INFO', response.data.plants);
                })
        },
        loadShifts: function ({commit, state, getters}, payload) {
            return axios.get('http://localhost:8000/' + payload.plant + '/' + payload.journal +'/get_shifts/',
                {
                    withCredentials: true
                })
                .then(response => {
                    state.events = response.data;
                    $(".fc-month-button").click();
                })
                .catch(e => {
                    console.log(e)
                });
        },
        sendUnsyncCell: function ({ commit, state, getters }, payload) {
            window.mv.$socket.sendObj({
                'type': 'shift_data',
                'cell_location': {
                    'group_id': getters.journalInfo.id,
                    'table_name': payload.tableName,
                    'field_name': payload.fieldName,
                    'index': payload.index
                },
                'value': payload.value
            })
        },
    }
}

export default journalState
