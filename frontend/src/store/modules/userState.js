import ajax from '../../axios.config';
import VueCookies from 'vue-cookies'

const userState = {
    namespaced: true,
    state: {
        user: null
    },
    getters: {
        user: state => state.user,
        username: state => state.user ? state.user.username : ''
    },
    mutations: {
        SET_USER (state, user) {
            state.user = user;
        }
    },
    actions: {
        login ({ commit, state, getters }, payload) {
            return new Promise((res, rej) => {
                ajax.post(window.HOSTNAME + '/api/auth/token/login/', {
                    username: payload.username,
                    password: payload.password
                })
                    .then((resp) => {
                        ajax.get(window.HOSTNAME + '/api/auth/users/me', {headers: {Authorization: 'Token ' + resp.data.auth_token}})
                            .then((userData) => {
                                commit('SET_USER', userData.data)
                            })
                            .then(() => {
                                VueCookies.set('Authorization', resp.data.auth_token, Infinity)
                            })
                            .then(() => {
                                res()
                            })
                            .catch(err => {
                                rej(err)
                            })
                    })
                    .catch(err => {
                        rej(err)
                    })
            })
        },
        logout ({ commit, state, getters }, payload) {
            return new Promise((res, rej) => {
                ajax.post(window.HOSTNAME + '/api/auth/token/logout/', null, {
                    headers: {Authorization: 'Token ' + VueCookies.get('Authorization')}
                })
                    .then(() => {
                        commit('SET_USER', null)
                    })
                    .then(() => {
                        VueCookies.set('Authorization', '')
                    })
                    .then(() => {
                        res()
                    })
            })
        }
    }
}

export default userState
