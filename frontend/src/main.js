import Vue from 'vue/dist/vue.esm.js'
import App from './App.vue'
import router from './router';
import store from './store/store';
import VueNativeSock from 'vue-native-websocket';

import './register-sw'
import './assets/js/index'

Vue.config.productionTip = false;

const dataEndpoint = 'ws://' + window.location.hostname + ':8000/e-logs/';
Vue.use(VueNativeSock, dataEndpoint, {
    store: store,
    format: 'json',
    reconnection: true,
    connectManually: true,
    passToStoreHandler: function (eventName, event) {
        if (eventName === 'SOCKET_onopen' && !this.store.getters['journalState/isSynchronized']) {
            let unsyncCells = this.store.getters['journalState/unsyncJournalCells']()

            unsyncCells.map(item => {
                this.store.dispatch('journalState/sendUnsyncCell', item)
            })

            this.store.commit('journalState/SET_SYNCHRONIZED', true)

            let plant = mv.$route.params.plant
            let journal = mv.$route.params.journal

            if (plant && journal) {
                setTimeout(() => {
                    this.store.dispatch('journalState/loadJournal', {
                      'plantName': plant,
                      'journalName': journal
                    })
                }, 2000)
        }
        }
        else if (eventName === 'SOCKET_onmessage') {
            let data = JSON.parse(event.data);
            this.store.commit('journalState/SAVE_CELL_VALUE', {
                tableName: data['cell_location']['table_name'],
                fieldName: data['cell_location']['field_name'],
                index: data['cell_location']['index'],
                value: data['value']
            })
        }
        else {
            return
        }

    }
});

window.mv = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
    mounted () {
    }
});
