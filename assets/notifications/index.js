import Vue from 'vue'
import App from './Messages.vue'

import Datetime from 'vue-datetime';

Vue.use(Datetime);

const vm = new Vue({
    el: '#messages-app',
    render: h => h(App)
 })