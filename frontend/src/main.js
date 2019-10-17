import Vue from 'vue/dist/vue.esm.js'
import App from './App.vue'
import router from './router';
import store from './store/store';
import VueNativeSock from 'vue-native-websocket';
import './register-sw'
import './assets/js/index'
import VueCookies from "vue-cookies";
import Notifications from 'vue-notification'
import EventBus from './EventBus'

import VTooltip from 'v-tooltip'

Vue.use(VTooltip);

Vue.use(Notifications);

Vue.config.performance = true;
Vue.config.productionTip = false;


if (process.env.NODE_ENV == 'production') {
    var dataEndpoint = 'wss://' + window.location.hostname + '/e-logs/';
    window.HOSTNAME = 'https://' + window.location.hostname;
    window.NODE_SERVER = 'https://' + window.location.hostname + ':3001';
    window.FRONT_CONSTRUCTOR_HOSTNAME = "https://" + window.location.hostname + ":8085";
} else {
    var dataEndpoint = 'ws://' + window.location.hostname + ':8000/e-logs/';
    window.HOSTNAME = 'http://' + window.location.hostname + ':8000';
    window.NODE_SERVER = 'http://' + window.location.hostname + ':3000';
    window.FRONT_CONSTRUCTOR_HOSTNAME = "http://" + window.location.hostname + ":8085";
}

Vue.use(VueNativeSock, dataEndpoint, {
    store: store,
    format: 'json',
    reconnection: true,
    connectManually: true,
    passToStoreHandler: function (eventName, event) {
        // console.log('event_data', event.data)
        if (eventName === 'SOCKET_onopen' && !this.store.getters['journalState/isSynchronized']) {
            let unsyncCells = this.store.getters['journalState/unsyncJournalCells']();
            console.log('unsyncCells', unsyncCells);
            unsyncCells.map((item, index) => {
                this.store.dispatch('journalState/sendUnsyncCell', item)
            })
        } else if (eventName === 'SOCKET_onmessage') {
            let data = JSON.parse(event.data);
            // console.log('data', JSON.parse(event.data))
            // console.log('event', event)
            if (data['type'] === 'shift_data') {
                let commitData = {'cells': []};
                let currentShift = this.store.getters['journalState/journalInfo'].id;
                for (let i in data['cells']) {
                    console.log(currentShift, data['cells'][i]['cell_location']['group_id']);
                    // accept only cells from current shift

                    if (currentShift !== data['cells'][i]['cell_location']['group_id']) {
                        continue
                    }
                    let cellData = data['cells'][i];

                    this.store.commit('journalState/ADD_RESPONSIBLE', cellData['responsible']);
                    // if received cell value is inputed by this user,
                    // store has it already
                    if (!(this.store.getters['userState/username'] in cellData['responsible'])) {
                        commitData['cells'].push({
                            tableName: cellData['cell_location']['table_name'],
                            fieldName: cellData['cell_location']['field_name'],
                            index: cellData['cell_location']['index'],
                            responsible: cellData['responsible'],
                            value: cellData['value']
                        })
                    }
                }
                if (commitData['cells'].length !== 0) {
                    this.store.commit('journalState/SAVE_CELLS', commitData)
                }
            }
            if (data['type'] === 'critical_value') {
                console.log('critical_value', data);

                if (data.cell) {
                    mv.$notify({
                        title: data.sendee[Object.keys(data.sendee)[0]],
                        text: 'Критическое значение ' + data.cell.field_name + ': "' + data.text + '"',
                        shiftId: data.shift_id,
                        duration: 5000,
                        type: 'warn'
                    });
                    this.store.dispatch('messagesState/loadUnreadedMessages');
                    this.store.dispatch('messagesState/loadMessages')
                }
            }
            if ((data['type'] === 'user_comment') || (data['type'] === 'system_comment')) {
                console.log('comment', data);
                let sendee = data.sendee ? data.sendee : data.employee;
                if (!Object.keys(sendee).includes(this.store.getters['userState/username'])) {
                    if (data['type'] === 'user_comment') {
                        mv.$notify({
                            title: sendee[Object.keys(sendee)[0]],
                            text: 'Комментарий к ячейке ' + data['cell']['field_name'] + ': "' + data.text + '"',
                            shiftId: data.shift_id,
                            duration: 5000,
                        });
                    }
                    this.store.dispatch('messagesState/loadUnreadedMessages');
                    this.store.dispatch('messagesState/loadMessages');
                    this.store.commit('journalState/SAVE_CELL_COMMENT', {
                        tableName: data['cell']['table_name'],
                        fieldName: data['cell']['field_name'],
                        index: data['cell']['index'],
                        comment: {
                            'text': data['text'],
                            'type': data['type'],
                            'created': Date.parse(data['created']),
                            'user': sendee
                        }
                    });

                    EventBus.$emit('scroll-to-bottom')
                }
            }
            if (data['type'] === 'set_mode') {
                console.log('set_mode', data);
                mv.$notify({
                    title: data.sendee[Object.keys(data.sendee)[0]],
                    text: 'Создан режим: "' + data.text + '"',
                    duration: 5000,
                });
                this.store.dispatch('messagesState/loadUnreadedMessages');
                this.store.dispatch('messagesState/loadMessages')
            }
        } else {

        }

    }
});

store.subscribe((mutation, state) => {
    if (!VueCookies.get('Authorization')) {
        router.push('/login')
    }
});

window.mv = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
    mounted() {
    }
});
