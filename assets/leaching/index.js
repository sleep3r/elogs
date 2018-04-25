import Vue from 'vue'
import App from './Densers.vue'

import Datetime from 'vue-datetime';

Vue.use(Datetime);

const vm = new Vue({
    el: '#leaching-app',
    render: h => h(App)
 })