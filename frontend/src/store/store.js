import Vue from 'vue'
import Vuex from 'vuex'
import journalState from './modules/journalState'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        journalState
    }
})