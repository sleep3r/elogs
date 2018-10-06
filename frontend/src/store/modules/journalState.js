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
                return state.plantsInfo.filter(item => item.name === state.journalInfo.plant.name)[0].verbose_name;
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
        cell: (state) => (tableName, fieldName, rowIndex) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                if (!(fieldName in fields)) {
                    // console.log('WARNING! Trying to get cell value of unexistent field: ' + fieldName);
                    return {};
                }
                let cells = fields[fieldName].cells;
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
            }
        },
        cellComments: (state) => (tableName, fieldName, rowIndex) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                if (!(fieldName in fields)) {
                    // console.log('WARNING! Trying to get cell comment of unexistent field: ' + fieldName);
                    return [];
                }
                let cells = fields[fieldName].cells;
                if (Object.keys(cells).length !== 0) {
                    if (rowIndex in cells) {
                        return cells[rowIndex].comments || [];
                    }
                    else {
                        // console.log('WARNING! Trying to get cell comment with unexistent index: ' + fieldName + ' ' + rowIndex);
                        return [];
                    }
                }
                else {
                    return [];
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
                        // find only non empty cells
                        if (fields[field].cells[index].value) {
                            max = (max < index) ? index : max;
                        }
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
        SAVE_CELLS (state, payload) {
            if (state.loaded) {
                let data = payload['cells']
                for (let i in data) {
                    let fields = state.journalInfo.journal.tables[data[i].tableName].fields;
                    if (!(data[i].fieldName in fields)) {
                        // console.log('WARNING! Trying to save value of unexistent field: ' + payload.fieldName);
                        // console.log('  Creating field ' + payload.fieldName + '...');
                        fields[data[i].fieldName] = {};
                        fields[data[i].fieldName]['cells'] = {};
                    }
                    let cells = fields[data[i].fieldName].cells;
                    if (data[i].index in cells) {
                        // update cell
                        cells[data[i].index]['value'] = data[i].value;
                        console.log('setting responsible')
                        console.log(data[i].responsible)
                        Vue.set(cells[data[i].index], 'responsible', data[i].responsible);
                        if (data[i].notSynchronized) {
                            cells[data[i].index]['notSynchronized'] = data[i].notSynchronized;
                            cells[data[i].index]['fieldName'] = data[i].fieldName;
                            cells[data[i].index]['tableName'] = data[i].tableName;
                            cells[data[i].index]['index'] = data[i].index;
                        }
                    }
                    else {
                        // create cell
                        Vue.set(cells, data[i].index, {});
                        Vue.set(cells[data[i].index], 'value', data[i].value);
                        Vue.set(cells[data[i].index], 'responsible', data[i].responsible);
                        if (data[i].notSynchronized) {
                            Vue.set(cells[data[i].index], 'notSynchronized', data[i].notSynchronized);
                        }
                    }
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
                        // update
                        if (!('comments' in cells[payload.index])) {
                            Vue.set(cells[payload.index], 'comments', []);
                        }
                        cells[payload.index]['comments'].push(payload.comment);
                    }
                    else {
                        // create cell
                        Vue.set(cells, payload.index, {'comments': []});
                        cells[payload.index]['comments'].push(payload.comment);
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
                                Vue.set(cells, i, {'value': ''});
                            }
                            if (i > payload.index) {
                                if (cells[i]) {
                                    Vue.set(cells, i-1, cells[i]);
                                    Vue.set(cells, i, {'value': ''});
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
                                    Vue.set(cells, i, {'value': ''})
                                }
                            }
                            if (i == payload.index) {
                                Vue.set(cells, i, {'value': ''})
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
                                Vue.set(cells, i, {'value': ''})
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
        sendJournalData: function ({ commit, state, getters }, payload) {
            // send all journal cells
            let data = {
                'type': 'shift_data',
                'cells': []
            }
            let tables = state.journalInfo.journal.tables
            for (let table in tables) {
                let fields = tables[table].fields
                    for (let field in fields) {
                        let cells = fields[field].cells
                        for (let index in cells) {
                            data.cells.push({
                                'cell_location': {
                                    'group_id': getters.journalInfo.id,
                                    'table_name': table,
                                    'field_name': field,
                                    'index': index
                                },
                                'value': cells[index].value
                            })
                        }
                    }
            }
            window.mv.$socket.sendObj(data)
        },
        loadJournal: function ({ commit, state, getters }, payload) {
            let id = payload['id'] ? payload['id'] : ''
            return axios
                .get(window.HOSTNAME+'/api/shifts/' + id, {
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
                .get(window.HOSTNAME+'/api/menu_info/')
                .then(response => {
                    commit('UPDATE_PLANTS_INFO', response.data.plants);
                })
        },
        loadShifts: function ({commit, state, getters}, payload) {
            return axios.get(window.HOSTNAME+'/' + payload.plant + '/' + payload.journal +'/get_shifts/',
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
