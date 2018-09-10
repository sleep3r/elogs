const journalState = {
  namespaced: true,
  state: {
    journal: {
        tables: []
    }
  },
  getters: {
      getJournalName (state, getters) {
        return state.journal.name
      },
      getCellMinValue (state, getters) {
        return function (tableName, cell) {
          let table = state.journal.tables.filter((item) => item.latinName === tableName)[0]
          let field = table.fields.filter(item => item.cell === cell)[0]
          if (field) {
              return field.min_value
          }
          else {
              return ''
          }
        }
      },
      getCellMaxValue (state, getters) {
        return function (tableName, cell) {
          let table = state.journal.tables.filter((item) => item.latinName === tableName)[0]
          let field = table.fields.filter(item => item.cell === cell)[0]
          if (field) {
              return field.max_value
          }
          else {
              return ''
          }
        }
      }
  },
  actions: {

  },
  mutations: {
    setJournal (state, payload) {
        state.journal = {...state.journal, ...payload}
    },
    addTable (state, payload) {
        state.journal.tables.push(payload)
    },
    setTable (state, payload) {
        let table = state.journal.tables.filter((item) => item.latinName === payload.tableName)[0]
        table.fields = payload.fields
    },
    setField (state, payload) {
        let table = state.journal.tables.filter((item) => item.latinName === payload.name)[0]
        let field = table.fields.filter(item => item.cell === payload.field.cell)[0]
        if(field) {
            field.field_name = payload.field.field_name
            field.min_value = payload.field.min_value
            field.max_value = payload.field.max_value
        }
        else table.fields.push(payload.field)

    }
  }
}

export default journalState