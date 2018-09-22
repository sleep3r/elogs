import $ from 'jquery'
import Vue from 'vue/dist/vue.esm.js'
import Plotly from 'plotly.js-dist'
import VueGridLayout from 'vue-grid-layout';
import Dashboard from '../tables/Dashboard.vue';

$(document).ready(() => {
    window.Plotly = Plotly
    window.dashboard = new Vue({
        el: '#vue-dashboard-container',
        components:{
            "Dashboard": Dashboard
        }
    })
});
