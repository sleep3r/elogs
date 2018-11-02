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

Vue.use(Notifications)

// import * as Sentry from '@sentry/browser';
// Sentry.init({
//     dsn: 'https://a86b628039394e4c89bea5b5b6835a8f@sentry.io/1299999',
//     integrations: [new Sentry.Integrations.Vue({ Vue })],
// });
// Sentry.configureScope((scope) => {
//     scope.setTag("server", "kazzink");
// });

Vue.config.productionTip = false;


if (process.env.NODE_ENV == 'production') {
    var dataEndpoint = 'wss://' + window.location.hostname + '/e-logs/'
    window.HOSTNAME = 'https://' + window.location.hostname
    window.NODE_SERVER = 'https://' + window.location.hostname + ':3000'
    window.FRONT_CONSTRUCTOR_HOSTNAME = "https://" + window.location.hostname + ":8085";
}
else {
    var dataEndpoint = 'ws://' + window.location.hostname + ':8000/e-logs/'
    window.HOSTNAME = 'http://' + window.location.hostname + ':8000'
    window.NODE_SERVER = 'http://' + window.location.hostname + ':3000'
    window.FRONT_CONSTRUCTOR_HOSTNAME = "http://" + window.location.hostname + ":8085";
}

Vue.use(VueNativeSock, dataEndpoint, {
    store: store,
    format: 'json',
    reconnection: true,
    connectManually: true,
    passToStoreHandler: function (eventName, event) {
        console.log('event', event)
        if (eventName === 'SOCKET_onopen' && !this.store.getters['journalState/isSynchronized']) {
            let unsyncCells = this.store.getters['journalState/unsyncJournalCells']()
            console.log('unsyncCells', unsyncCells)
            unsyncCells.map((item, index) => {
                this.store.dispatch('journalState/sendUnsyncCell', item)
            })

            // let plant = mv.$route.params.plant
            // let journal = mv.$route.params.journal

            // if (plant && journal) {
            //     setTimeout(() => {
            //         if (window.mv.$route.params.shift_id) {
            //           this.store.dispatch('journalState/loadJournal', {'id': window.mv.$route.params.shift_id})
            //               .then(() => {
            //                   this.store.commit('journalState/SET_SYNCHRONIZED', true)
            //               })
            //         }
            //         else if (plant && journal) {
            //             this.store.dispatch('journalState/loadJournal', {
            //               'plantName': plant,
            //               'journalName': journal
            //             })
            //                 .then(() => {
            //                     this.store.commit('journalState/SET_SYNCHRONIZED', true)
            //                 })
            //         }
            //     }, unsyncCells.length * 100)
            // }
        }
        else if (eventName === 'SOCKET_onmessage') {
            let data = JSON.parse(event.data);
            // console.log('data', JSON.parse(event.data))
            // console.log('event', event)
            if (data['type'] == 'shift_data') {
                console.log('shift_data', data)

                let commitData = {'cells': []}
                for (let i in data['cells']) {
                    let cellData = data['cells'][i]

                    this.store.commit('journalState/ADD_RESPONSIBLE', cellData['responsible'])
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
                console.log(commitData)
                if (commitData['cells'].length !== 0) {
                    this.store.commit('journalState/SAVE_CELLS', commitData)
                }
            }
            if (data['type'] === 'messages') {
                console.log(data);

                if (data.cell) {
                    mv.$notify({
                        title: data.sendee[Object.keys(data.sendee)[0]],
                        text: data.cell + ': ' + data.text,
                        duration: 5000,
                        type: 'warn'
                    })

                    this.store.dispatch('messagesState/loadUnreadedMessages')
                    this.store.dispatch('messagesState/loadMessages')
                }
                else {
                    let sendee = data.sendee ? data.sendee : data.employee
                    if (!Object.keys(sendee).includes(this.store.getters['userState/username'])) {
                        // mv.$notify({
                        //     title: sendee[Object.keys(sendee)[0]],
                        //     text: data['cell_location']['field_name'] + ': ' + data.message.text,
                        //     duration: 5000,
                        // })

                        this.store.commit('journalState/SAVE_CELL_COMMENT', {
                            tableName: data['cell_location']['table_name'],
                            fieldName: data['cell_location']['field_name'],
                            index: data['cell_location']['index'],
                            comment: {
                                'text': data['message']['text'],
                                'created': Date.parse(data['created']),
                                'user': sendee
                            }
                        });

                        EventBus.$emit('scroll-to-bottom')
                    }
                }
            }
        }
        else {
            return
        }

    }
});

store.subscribe((mutation, state) => {
    if (!VueCookies.get('Authorization')) {
        router.push('/login')
    }
})

window.mv = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
    mounted() {
    }
});
