const journalState = {
  namespaced: true,
  state: {
    journal: {
        tables: []
    }
  },
  getters: {
      getJournal (state, getters) {
          return state.journal
      },
      getJournalName (state, getters) {
        return state.journal.name
      },
      getTables (state, getters) {
        return state.journal.tables
      },
      getTableHTML (state, getters) {
          return function (tableName) {
              let table = state.journal.tables.filter((item) => item.name === tableName)[0]
              return table.html
          }
      },
      getTableRepeatableRow (state, getters) {
          return function (tableName) {
              let table = state.journal.tables.filter((item) => item.name === tableName)[0]
              return table.repeatable_row
          }
      },
      getCellMinValue (state, getters) {
        return function (tableName, cell) {
          let table = state.journal.tables.filter((item) => item.name === tableName)[0]
          let field = table.fields.filter(item => item.cell === cell)[0]
          if (field && field.min_value) {
              return field.min_value
          }
          else {
              return ''
          }
        }
      },
      getCellMaxValue (state, getters) {
        return function (tableName, cell) {
          let table = state.journal.tables.filter((item) => item.name === tableName)[0]
          let field = table.fields.filter(item => item.cell === cell)[0]
          if (field && field.max_value) {
              return field.max_value
          }
          else {
              return ''
          }
        }
      },
      getCellType (state, getters) {
          return function (tableName, cell) {
              let table = state.journal.tables.filter((item) => item.name === tableName)[0]
              let field = table.fields.filter(item => item.cell === cell)[0]
              if (field && field.type) {
                  return field.type
              }
              else {
                  return ''
              }
          }
      },
      getCellUnits (state, getters) {
          return function (tableName, cell) {
              let table = state.journal.tables.filter((item) => item.name === tableName)[0]
              let field = table.fields.filter(item => item.cell === cell)[0]
              if (field && field.units) {
                  return field.units
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
    deleteTable (state, payload) {
        state.journal.tables = state.journal.tables.filter(item => item.name !== payload.tableName)
    },
    setTable (state, payload) {
        let table = state.journal.tables.filter((item) => item.name === payload.tableName)[0]
        table = Object.assign(table, {...payload.data})
    },
    setTablesList (state, payload) {
        state.journal.tables = payload.tables
    },
    setFields (state, payload) {
        let table = state.journal.tables.filter((item) => item.name === payload.name)[0]

        payload.fields.cells.map(cell => {
            let field = table.fields.filter(item => item.cell === $(cell).attr('id'))[0]

            if (field) {
                field.field_name = payload.fields.field_name
                field.min_value = payload.fields.min_value
                field.max_value = payload.fields.max_value
                field.type = payload.fields.type
                field.units = payload.fields.units
            }
        })

    }
  }
}

export default journalState