import ajax from '../../axios.config';
import VueCookies from 'vue-cookies'

const messagesState = {
    namespaced: true,
    state: {
        messages: [],
        unreadedMessages: []
    },
    getters: {
        messages: state => state.messages,
        unreadedMessages: state => state.unreadedMessages,
        highlightOnLoad: state => state.highlight_on_load
    },
    mutations: {
        SET_MESSAGES (state, messages) {
            state.messages = messages
        },
        SET_UNREADED_MESSAGES (state, messages) {
            state.unreadedMessages = messages
        },
        ADD_MESSAGE (state, msg) {
            state.messages.push(msg)
        },
        ADD_UNREADED_MESSAGE (state, msg) {
            state.unreadedMessages.push(msg)
        },
        READ_MESSAGE (state, id) {
            state.unreadedMessages = state.unreadedMessages.filter(item => item.id !== id)
        },
        HIGHLIGHT_CELL_ON_TABLE_LOAD (state, payload) {
            Vue.set(state, 'highlight_on_load', payload)
        },
    },
    actions: {
        loadMessages ({ commit, state, getters }, payload) {
            return ajax.get(window.HOSTNAME + '/api/messages/list', {
                headers: {Authorization: 'Token ' + VueCookies.get('Authorization')}
            })
                .then((res) => {
                    commit('SET_MESSAGES', res.data)
                })
                .catch(err => {
                    console.log(err)
                })
        },
        readMessage ({ commit, state, getters }, payload) {
            return ajax.put(window.HOSTNAME + '/api/messages/?id=' + payload.id, null, {
                headers: {Authorization: 'Token ' + VueCookies.get('Authorization')}
            })
                .then((res) => {
                    commit('READ_MESSAGE', payload.id)
                })
                .catch(err => {
                    console.log(err)
                })
        },
        loadUnreadedMessages ({ commit, state, getters }, payload) {
            return ajax.get(window.HOSTNAME + '/api/messages', {
                headers: {Authorization: 'Token ' + VueCookies.get('Authorization')}
            })
                .then((res) => {
                    commit('SET_UNREADED_MESSAGES', res.data)
                })
                .catch(err => {
                    console.log(err)
                })
        }
    }
}

export default messagesState
