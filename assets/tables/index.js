import Vue from 'vue/dist/vue.esm.js'
import VueNativeSock from 'vue-native-websocket'
import TableCommon from './TableCommon.vue';
import JournalPanel from './JournalPanel.vue';
import { store } from './store';


Vue.component('tablecommon', TableCommon);
Vue.component('journal-panel', JournalPanel);

const dataEndpoint = 'ws://' + window.location.host + '/journal_info/';
Vue.use(VueNativeSock, dataEndpoint, { store: store, format: 'json', reconnection: true, connectManually: true });

window.app = new Vue({
  el: '#elogs-app',
  store: store,
  components: { TableCommon },
  delimiters: ['%{', '}'],
  mounted () {
    this.$connect();
    store.dispatch('loadJournal');
  }
});
