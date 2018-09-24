import Vue from 'vue/dist/vue.esm.js'
import TableCommon from './TableCommon.vue';
import JournalPanel from './JournalPanel.vue';
import { store } from './store';


Vue.component('tablecommon', TableCommon);
Vue.component('journal-panel', JournalPanel);


window.app = new Vue({
  el: '#elogs-app',
  store: store,
  components: {
      "TableCommon": TableCommon,
  },
  delimiters: ['%{', '}'],
  mounted () {
    store.dispatch('loadJournal');
  }
});
