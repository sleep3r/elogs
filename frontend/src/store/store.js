import Vue from 'vue/dist/vue.esm.js'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import journalState from './modules/journalState'
import userState from './modules/userState'
import modesState from './modules/modesState'

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        journalState,
        userState,
        modesState
    },
    plugins: [vuexLocal.plugin]
})