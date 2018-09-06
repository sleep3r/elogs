import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
    strict: true,
    state: {
      pageId: 0,
      plantName: '',
      journalName: '',
      journalInfo: {},
      syncronized: false,
    },
    getters: {
      tables: state => {
        if (Object.keys(state.journalInfo).length !== 0) {
          return Object.keys(state.journalInfo.journal.tables);
        } else {
          return [];
        }
      },
      journalName: state => {
        if (Object.keys(state.journalInfo).length !== 0) {
          return state.journalInfo.journal.name;
        } else {
          return '';
        }
      }
    },
    mutations: {
      updateJournalInfo (state, journalInfo) {
        state.journalInfo = journalInfo
      }
    },
    actions: {

    }
});
