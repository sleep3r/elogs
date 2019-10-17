import Vue from 'vue/dist/vue.esm.js'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import journalState from './modules/journalState'
import formulaState from './modules/formulaState'
import userState from './modules/userState'
import modesState from './modules/modesState'
import settingsState from './modules/settingsState'
import messagesState from './modules/messagesState'
import VueCookies from "vue-cookies";

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
});

Vue.use(Vuex);

let store = new Vuex.Store({
    modules: {
        journalState,
        formulaState,
        userState,
        modesState,
        settingsState,
        messagesState
    },
    plugins: [vuexLocal.plugin]
});

export default store
