import Vue from 'vue/dist/vue.esm.js'
import VueNativeSock from 'vue-native-websocket'
import TableCommon from './TableCommon.vue';
import JournalPanel from './JournalPanel.vue';
import { store } from './store';


Vue.component('tablecommon', TableCommon);
Vue.component('journal-panel', JournalPanel);


const dataEndpoint = 'ws://' + window.location.host + '/shift/' + window.location.pathname.split("/")[3];
Vue.use(VueNativeSock, dataEndpoint, {
  store: store,
  format: 'json',
  reconnection: true,
  connectManually: true,
  passToStoreHandler: function (eventName, event) {
    console.log(eventName)
    if (!(eventName === 'SOCKET_onmessage')) { return }
    console.log('in onmessage')
    let data = JSON.parse(event.data);
    console.log(data)
    this.store.commit('SAVE_CELL_VALUE', {
      tableName: data['cell_location']['table_name'],
      fieldName: data['cell_location']['field_name'],
      index: data['cell_location']['index'],
      value: data['value']
    })
  }
})

window.tablesApp = new Vue({
  el: '#elogs-app',
  store: store,
  components: { TableCommon },
  delimiters: ['%{', '}'],
  mounted () {
    this.$connect();
    store.dispatch('loadJournal');
  }
});
