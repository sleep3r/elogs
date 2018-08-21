import Vue from 'vue'
import App from './Messages.vue'

import Datetime from 'vue-datetime';

Vue.use(Datetime);

$(document).ready(() => {
    const vm = new Vue({
        el: '#messages-app',
        render: h => h(App)
    });
    window.vm = vm;
});
