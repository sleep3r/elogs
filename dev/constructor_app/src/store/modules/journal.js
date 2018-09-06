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
    setField (state, payload) {
        let table = state.journal.tables.filter((item) => item.latinName === payload.name)[0]
        if (table.fields.length) {
            let field = table.fields.filter(item => item.cell === payload.field.cell)[0]
            console.log(field, payload.field)
            if(field) {
                field.field_name = payload.field.field_name
                field.min_value = payload.field.min_value
                field.max_value = payload.field.max_value
            }
            else table.fields.push(payload.field)

        }
        else table.fields.push(payload.field)

    }
  }
}

export default journalState