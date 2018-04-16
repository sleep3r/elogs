import Vue from 'vue'
import App from './App.vue'

import VModal from 'vue-js-modal'
Vue.use(VModal, { dynamic: true })

import Datetime from 'vue-datetime';

Vue.use(Datetime);

const vm = new Vue({
    el: '#spa-index',
    render: h => h(App)
 })