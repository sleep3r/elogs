import Vue from 'vue'
import App from './Furnace.vue'

import VModal from 'vue-js-modal'
Vue.use(VModal, { dynamic: true })

import Datetime from 'vue-datetime';

Vue.use(Datetime);

const vm = new Vue({
    el: '#furnace-index',
    render: h => h(App)
 })