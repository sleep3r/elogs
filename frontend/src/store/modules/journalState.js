import ajax from '../../axios.config'
import VueCookies from 'vue-cookies'
import {getValue} from '../../assets/js/formula'
var FormulaParser = require('hot-formula-parser').Parser;

const journalState = {
    namespaced: true,
    state: {
        tablesHTML: [],
        plantsInfo: [],
        journalInfo: {},
        events: [],
        loaded: false,
        socket: {
            isConnected: false,
            reconnectError: false,
        },
        isSynchronized: true,
        isForPrint: false
    },
    getters: {
        loaded: state => state.loaded,
        isForPrint: state => state.isForPrint,
        journalInfo: state =>  state.journalInfo,
        events: state =>  state.events,
        currentMode: state => {
            if (state.loaded) {
                return state.journalInfo.journal.mode;
            } else {
                return '';
            }
        },
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
        journalVersion: state => {
            if (state.loaded) {
                return state.journalInfo.version;
            } else {
                return -1;
            }
        },
        journalVerboseName: (state, getters) => {
            if (state.loaded) {
                let plant = getters['plantName']
                return state.plantsInfo.filter(item => item.name === plant)[0].journals.filter(item => item.name === state.journalInfo.journal.name)[0].verbose_name;
            } else {
                return '';
            }
        },
        shiftID: state => {
            if (state.loaded) {
                return state.journalInfo.id;
            } else {
                return -1;
            }

        },
        tableVerboseName: (state) => (tableName) => {
            if (state.loaded) {
                let table = state.journalInfo.journal.tables[tableName]
                if (table) {
                    return table.title
                }
                else {
                    return ''
                }
            } else {
                return '';
            }
        },
        constraintsModes: state => {
            if (state.loaded) {
                return state.journalInfo.field_constraints_modes.modes
            }
        },
        constraintsModeIsActive: (state) => (id) => {
            if (state.loaded) {
                var modes = state.journalInfo.field_constraints_modes.modes
                for (let i in modes) {
                    if (modes[i]['id'] == id) {
                        return modes[i].is_active
                    }
                }
            }
        },
        currentConstraintsMode: state => {
            if (state.loaded) {
                var id = state.journalInfo.field_constraints_modes.current_mode
                var modes = state.journalInfo.field_constraints_modes.modes
                for (let i in modes) {
                    if (modes[i]['id'] == id) {
                        return modes[i]
                    }
                }
                return null
            }
        },
        currentConstraintsModeId: state => {
            if (state.loaded) {
                return state.journalInfo.field_constraints_modes.current_mode || null
            }
        },
        fieldVerboseName: (state) => (tableName, fieldName) => {
            if (state.loaded
                && state.journalInfo.journal.tables[tableName].fields[fieldName] !== void 0
                && Object.keys(state.journalInfo.journal.tables[tableName].fields[fieldName]).indexOf('title')
                ) {
                    return state.journalInfo.journal.tables[tableName].fields[fieldName].title;
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
                let field = fields[fieldName];
                if (field.formula) {
                    window.parser.setFunction("FUNC", getValue.bind({
                        journal: state.journalInfo.journal.name,
                        table: tableName,
                        field: fieldName,
                        index: rowIndex,
                        shift: 0,
                        isTableIndexed: false,
                    }))// Timout for sequential functions execution
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
                        // table comment is stored s cell, but shouldn't be counted as cell
                        if ((fields[field].cells[index].value)&&(field !== '__table__comment')) {
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
            // console.log('fieldName', fieldName)
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                // console.log('fields', fields)
                if (!(fieldName in fields)) {
                    // console.log("WARNING! Trying to get field desctiption of unexistent field: " + fieldName);
                    return {};
                }
                return fields[fieldName].field_description || ''
            }
            else {
                return ''
            }
        },
        fieldConstraints: (state) => (tableName, fieldName, constraintsMode) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                // console.log('fields', fields)
                if (!(fieldName in fields)) {
                    // console.log("WARNING! Trying to get field desctiption of unexistent field: " + fieldName);
                    return {};
                }
                var fieldConstraintsModes = state.journalInfo.field_constraints_modes.modes
                var desc = fields[fieldName].field_description
                if (typeof desc == "undefined") {
                    return {}
                }
                var fieldConstraints = desc['constraints_modes']
                if (typeof fieldConstraints == "undefined") {
                    return {}
                }
                // console.log(fieldConstraints)

                // if constraintsMode is not null and constraints for this field exist
                if (constraintsMode) {
                    return fieldConstraints[constraintsMode] || {}
                }
                else {
                    for (var i in fieldConstraintsModes) {
                        var mode = fieldConstraintsModes[i]['id']
                        var modeIsActive = fieldConstraintsModes[i]['is_active']
                        // if mode is active and field has this mode
                        console.log(mode, modeIsActive)
                        if ((modeIsActive) && (typeof fieldConstraints[mode] !== 'undefined')) {
                            return fieldConstraints[mode]
                        }
                    }
                }
                return {}
            }
            else {
                return ''
            }
        },
        fieldFormula: (state) => (tableName, fieldName) => {
            if (state.loaded) {
                let fields = state.journalInfo.journal.tables[tableName].fields;
                if (!(fieldName in fields)) {
                    // console.log("WARNING! Trying to get field desctiption of unexistent field: " + fieldName);
                    return '';
                }
                return fields[fieldName].formula || ''
            }
            else {
                return ''
            }
        },
        tableHTML: (state) => (payload) => {
            if (state.loaded) {
                let tableItem = state.tablesHTML.filter(item =>
                    item.plant === payload.plant && item.journal === payload.journal && item.table === payload.table)[0]
                if (tableItem) {
                    return tableItem.html
                }
                else {
                    return ''
                }
            }
            else {
                return ''
            }
        }

    },
    mutations: {
        SET_FOR_PRINT (state, isForPrint) {
            state.isForPrint = isForPrint
        },
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
        ADD_RESPONSIBLE (state, payload) {
            let responsibles = state.journalInfo.responsibles
            if (typeof responsibles == "undefined") {
                responsibles = [ payload ]
            }
            let currentResp = responsibles.filter(item => Object.keys(item)[0] == Object.keys(payload)[0])[0]
            if (!currentResp) {
                state.journalInfo.responsibles.push(payload)
            }
        },
        REMOVE_PERMISSION (state, payload) {
            var permissions = state.journalInfo.permissions.permissions
            var index = permissions.indexOf(payload);
            console.log('index of permission: ' + index)
            if (index !== -1) permissions.splice(index, 1);
        },
        SAVE_CELLS (state, payload) {
            if (state.loaded) {
                let data = payload['cells']
                for (let i in data) {
                    let fields = state.journalInfo.journal.tables[data[i].tableName].fields;
                    if (!(data[i].fieldName in fields)) {
                        // console.log('WARNING! Trying to save value of unexistent field: ' + payload.fieldName);
                        // console.log('  Creating field ' + payload.fieldName + '...');
                        Vue.set(fields, data[i].fieldName, {});
                        Vue.set(fields[data[i].fieldName], 'cells', {});
                    }
                    let cells = fields[data[i].fieldName].cells;
                    if (data[i].index in cells) {
                        // update cell
                        cells[data[i].index]['value'] = data[i].value;
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
                        Vue.set(cells[data[i].index], 'fieldName', data[i].fieldName);
                        Vue.set(cells[data[i].index], 'tableName', data[i].tableName);
                        Vue.set(cells[data[i].index], 'index', data[i].index);
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
        SET_CONSTRAINTS_MODE (state, id) {
            if (state.loaded) {
                // current mode is mode that user is editing now
                Vue.set(state.journalInfo.field_constraints_modes, 'current_mode', id)
            }
        },
        SET_CONSTRAINT (state, payload) {
            if (state.loaded) {
                var field = state.journalInfo.journal.tables[payload['tableName']].fields[payload.fieldName]
                if ("constraints_modes" in field.field_description) {
                    var fieldConstraints = field.field_description.constraints_modes[payload['mode']]
                    if (fieldConstraints) {
                        Vue.set(fieldConstraints, payload['constraintType'], payload['constraintValue'])
                    }
                    else {
                        Vue.set(field.field_description.constraints_modes, payload['mode'], {})
                        var fieldConstraints = field.field_description.constraints_modes[payload['mode']]
                        Vue.set(fieldConstraints, payload['constraintType'], payload['constraintValue'])
                    }
                }
                else {
                    Vue.set(field.field_description, "constraints_modes", {})
                    Vue.set(field.field_description.constraints_modes, payload['mode'], {})
                    var fieldConstraints = field.field_description.constraints_modes[payload['mode']]
                    Vue.set(fieldConstraints, payload['constraintType'], payload['constraintValue'])
                }

            }
        },
        ADD_CONSTRAINT (state, payload) {
            if (state.loaded) {
                state.journalInfo.field_constraints_modes.modes.push({
                    id: payload.id,
                    message: payload.message,
                    is_active: payload.is_active
                })
            }
        },
        TOGGLE_CONSTRAINTS_MODE (state, payload) {
            if (state.loaded) {
                var constraintModes = state.journalInfo.field_constraints_modes.modes
                for (let i=0; i<constraintModes.length; i++) {
                    if (constraintModes[i].id == payload.id) {
                        constraintModes[i]['is_active'] = payload.active
                    }
                }
            }
        },
        DELETE_CONSTRAINTS_MODE (state, payload) {
          if (state.loaded) {
              var constraintModes = state.journalInfo.field_constraints_modes.modes
              for (let i=0; i<constraintModes.length; i++) {
                  if (constraintModes[i].id == payload.id) {
                      constraintModes.splice(i, 1);
                  }
              }
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
        ADD_TABLE_HTML (state, payload) {
            state.tablesHTML.push({
                plant: payload.plant,
                journal: payload.journal,
                table: payload.table,
                html: payload.html
            })
        },
        UPDATE_TABLE_HTML (state, payload) {
            let table = state.tablesHTML.filter(item =>
                item.plant === payload.plant && item.journal === payload.journal && item.table === payload.table)[0]
            table.html = payload.html
        },
        SET_EVENTS (state, payload) {
            state.events = payload
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
                'final': true,
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
            commit('SET_LOADED', false);
            let id = payload['id'] ? payload['id'] : ''
            return ajax
                .get(window.HOSTNAME+'/api/shifts/' + id, {
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
            ajax
                .get(window.HOSTNAME+'/api/menu_info/')
                .then(response => {
                    commit('UPDATE_PLANTS_INFO', response.data.plants);
                })
        },
        loadShifts: function ({commit, state, getters}, payload) {
            return ajax.get(window.HOSTNAME + '/api/' + payload.plant + '/' + payload.journal +'/get_groups/')
                .then(response => {
                    commit('SET_EVENTS', response.data)
                    $(".fc-month-button").click();
                })
                .catch(e => {
                    console.log(e)
                });
        },
        sendUnsyncCell: function ({ commit, state, getters }, payload) {
            console.log('unsyncCell', payload)
            window.mv.$socket.sendObj({
                'type': 'shift_data',
                'unsync':true,
                'cells':[{
                'cell_location': {
                    'group_id': getters.journalInfo.id,
                    'table_name': payload.tableName,
                    'field_name': payload.fieldName,
                    'index': payload.index
                    },
                'value': payload.value }],
            })
        },
    }
}

export default journalState
