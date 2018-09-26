import Vue from 'vue/dist/vue.esm.js'
import App from './App.vue'
import router from './router';
import store from './store/store';
import VueNativeSock from 'vue-native-websocket';

import './register-sw'
import './assets/js/index'

Vue.config.productionTip = false

const dataEndpoint = 'ws://localhost:8000' + '/e-logs/?shift=' + window.location.pathname.split("/")[3];
Vue.use(VueNativeSock, dataEndpoint, {
    store: store,
    format: 'json',
    reconnection: true,
    connectManually: true,
    passToStoreHandler: function (eventName, event) {
        if (!(eventName === 'SOCKET_onmessage')) { return }
        let data = JSON.parse(event.data);
        this.store.commit('journalState/SAVE_CELL_VALUE', {
            tableName: data['cell_location']['table_name'],
            fieldName: data['cell_location']['field_name'],
            index: data['cell_location']['index'],
            value: data['value']
        })
    }
})

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
    mounted () {
        this.$connect();
    }
})
