import axios from 'axios';
import Vue from 'vue/dist/vue.esm.js';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
    strict: true,
    state: {
      journalInfo: {},
      loaded: false,
      socket: {
        isConnected: false,
        reconnectError: false,
      }
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
            console.log('WARNING! Trying to get cell value of unexistent field: ' + fieldName);
            return '';
          }
          let cells = fields[fieldName].cells;
          if (Object.keys(cells).length !== 0) {
            if (rowIndex in cells) {
              return cells[rowIndex].value;
            }
            else {
              console.log('WARNING! Trying to get cell value with unexistent index: ' + fieldName + ' ' + rowIndex);
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
            console.log('WARNING! Trying to get cell comment of unexistent field: ' + fieldName);
            return '';
          }
          let cells = fields[fieldName].cells;
          if (Object.keys(cells).length !== 0) {
            if (rowIndex in cells) {
              return cells[rowIndex].comment;
            }
            else {
              console.log('WARNING! Trying to get cell comment with unexistent index: ' + fieldName + ' ' + rowIndex);
              return '';
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
          for (let field in fields) {
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
      SET_PAGE_MODE (state, mode) {
        state.journalInfo.mode = mode
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
          if (payload.value) {
            if (payload.index in cells) {
              // update cell
              cells[payload.index]['value'] = payload.value;
            }
            else {
              // create cell
              Vue.set(cells, payload.index, {});
              Vue.set(cells[payload.index], 'value', payload.value);
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
            console.log('WARNING! Trying to save comment of unexistent field: ' + payload.fieldName);
            console.log('  Creating field ' + payload.fieldName + '...');
            fields[payload.fieldName] = {};
            fields[payload.fieldName]['cells'] = {};
          }
          let cells = fields[payload.fieldName].cells;
          if (payload.comment) {
            if (payload.index in cells) {
              // update cell
              cells[payload.index]['comment'] = payload.comment;
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
      loadJournal: function () {
        axios
          .get('/api/shifts/' + window.location.pathname.split("/")[3])
          .then(response => {
            store.commit('UPDATE_JOURNAL_INFO', response.data);
            store.commit('SET_LOADED', true);
          })
      },
    }
});
