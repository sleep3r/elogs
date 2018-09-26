import Vue from 'vue/dist/vue.esm.js'
import App from './App.vue'
import router from './router';
import store from './store/store';

import './register-sw'
import './assets/js/index'

Vue.config.productionTip = false

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
})
