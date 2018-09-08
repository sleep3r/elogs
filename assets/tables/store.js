import axios from 'axios';
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
    strict: true,
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
          let cells = state.journalInfo.journal.tables[tableName].fields[fieldName].cells;
          if (Object.keys(cells).length !== 0) {
              if (rowIndex in cells) {
                  return cells[rowIndex].value
              }
          }
          else {
            return ''
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
                max = max < index ? index : max
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
            return state.journalInfo.journal.tables[tableName].fields[fieldName].field_description || ''
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
          let cells = state.journalInfo.journal.tables[payload.tableName].fields[payload.fieldName].cells;
          if (payload.index in cells) {
            // update cell
            console.log('update cell')
            cells[payload.index]['value'] = payload.value;
            console.log(state)
          }
          else {
            // create cell
            cells[payload.index] = {}
            cells[payload.index]['value'] = payload.value;
          }
        }
      }
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
