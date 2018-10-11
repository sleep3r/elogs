import Vue from 'vue/dist/vue.esm.js'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import journalState from './modules/journalState'
import userState from './modules/userState'
import modesState from './modules/modesState'
import settingsState from './modules/settingsState'
import VueCookies from "vue-cookies";

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})

Vue.use(Vuex)

let store = new Vuex.Store({
    modules: {
        journalState,
        userState,
        modesState,
        settingsState
    },
    plugins: [vuexLocal.plugin]
})

export default store