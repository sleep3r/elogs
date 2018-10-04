import axios from 'axios'
import VueCookies from "vue-cookies";

const NOT_FOUND = -1;

const settingsState = {
  namespaced: true,
  state: {
        settings: [],
        searchByName: '',
        currentModel: ''
  },
  getters: {
    searchByName: state => state.searchByName,
    currentModel: state => state.currentModel,
    getSettings: state => {
      return state.settings;
    },
    favorites: state => {
      return state.settings.filter((v)=> v.isFavorite)
    },
    filtredByName: state => {
        if (state.searchByName.length > 0) {
            return state.settings.filter((v) => (v.scope.name.indexOf(state.searchByName) > NOT_FOUND))
        } else {
          return state.settings;
        }
    }
  },
  mutations: {
    SET_CURRENT_MODEL: (state, model) => {
      state.currentModel = model
    },
    SET_SETTINGS: (state, settings) => {
      state.settings = settings;
    },
    SET_SEARCH_BY_NAME: (state, text) => {
      state.searchByName = text;
    }
  },
  actions: {
      setCurrentModel: function () {

      },
      loadSettings: function({ commit, state, getters }, payload) {
        let url = 'http://localhost:8000/api/settings/';
        return axios.get(url, {withCredentials: true })
             .then((response) => {
                let settings = response.data.settings;
                for (let set of settings) {
                    set.isFavorite = false;
                }
                commit('SET_SETTINGS', settings);
             })
      },
      addSetting: function({commit, state, getters}, payload) {
          console.log("addSetting", payload);
      },
      updateSetting: function ({commit, state, getters}, payload) {
          console.log("updateSetting", payload, "state: ", state, 'getters', getters);
          let url = 'http://localhost:8000/api/settings/';

          return axios.post(url, payload)
              .then((response) => { console.log(response)})
              .catch((err) => {
                    console.log(err)
                })
      }
  }
};

export default settingsState