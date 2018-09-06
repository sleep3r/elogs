import Vue from 'vue/dist/vue.esm.js'
import TableCommon from './TableCommon.vue';
import axios from 'axios';


Vue.component('tablecommon', TableCommon);

window.app = new Vue({
  el: '#elogs-app',
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
      if (this.journalInfo) {
          console.log(this.journalInfo.journal.tables.keys());
          return this.journalInfo.journal.tables.keys();
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
        })
    },
  },
  mounted () {
    this.plantName = window.location.pathname.split("/")[1];
    this.journalName = window.location.pathname.split("/")[2];
    this.pageId = window.location.pathname.split("/")[3];
    this.loadJournal();
  }
});
