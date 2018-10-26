import ajax from '../../axios.config';
import VueCookies from 'vue-cookies'

const userState = {
    namespaced: true,
    state: {
        user: null
    },
    getters: {
        user: state => state.user,
        username: state => state.user ? state.user.username : '',
        fullname: state => state.user ? state.user.full_name: '',
        isSuperuser: state => state.user ? state.user.is_superuser : false,
        isBoss: state => state.user ? state.user.is_boss : false,
        hasPerm: state => perm => state.user && state.user.is_boss ? state.user.is_boss.includes(perm) : false
    },
    mutations: {
        SET_USER (state, user) {
            state.user = user;
        }
    },
    actions: {
        login ({ commit, state, getters }, payload) {
            return ajax.post(window.HOSTNAME + '/api/auth/token/login/', {
                username: payload.username,
                password: payload.password
            })
                .then((resp) => {
                    return ajax.get(window.HOSTNAME + '/api/auth/users/me', {headers: {Authorization: 'Token ' + resp.data.auth_token}})
                        .then((userData) => {
                            commit('SET_USER', userData.data)
                            return userData
                        })
                        .then((res) => {
                            VueCookies.set('Authorization', resp.data.auth_token, Infinity)
                            return res
                        })
                        .then((res) => {
                            return res
                        })
                        .catch(err => {
                            return err
                        })
                })
                .catch(err => {
                    return err
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
