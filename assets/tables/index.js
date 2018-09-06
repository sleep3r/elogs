import Vue from 'vue/dist/vue.esm.js'
import TableCommon from './TableCommon.vue';
import axios from 'axios';
import { store } from './store';


Vue.component('tablecommon', TableCommon);

window.app = new Vue({
  el: '#elogs-app',
  store: store,
  components: { TableCommon },
  data: function () {
    return {
      pageId: '',
      plantName: '',
      journalName: '',
      journalInfo: {},
      syncronized: false,
    }
  },
  delimiters: ['%{', '}'],
  computed: {
    tables: function () {
      if (Object.keys(this.journalInfo).length !== 0) {
          console.log('tables from store:');
          console.log(store.getters.tables);
          return Object.keys(this.journalInfo.journal.tables);
      } else {
        return [];
      }
    }
  },
  methods: {
    loadJournal: function () {
      this.syncronized = false;
      axios
        .get('/api/shifts/' + this.pageId)
        .then(response => {
          this.syncronized = true;
          this.journalInfo = response.data;
          store.commit('updateJournalInfo', response.data);
        })
    },
  },
  mounted () {
    console.log('Tables were mounted')
    this.plantName = window.location.pathname.split("/")[1];
    this.journalName = window.location.pathname.split("/")[2];
    this.pageId = window.location.pathname.split("/")[3];
    this.loadJournal();
  }
});
