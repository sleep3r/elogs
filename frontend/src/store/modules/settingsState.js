import axios from 'axios'

const NOT_FOUND = -1;

function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

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
      // return state.settings;
        return state.settings.filter((v) => (v.name === 'field_description'))
    },
    favorites: state => {
      return state.settings.filter((v)=> v.isFavorite)
    },
    filtredByName: state => {
        if (state.searchByName.length > 0) {
            return state.settings.filter((v) => (v.scope.name.indexOf(state.searchByName) > NOT_FOUND && v.name === 'field_description'))
        } else {
          return state.settings.filter((v) => (v.name === 'field_description'))
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
    },
    UPDATE_MODEL_VALUE: (state, payload) => {
        let model = JSON.parse(JSON.stringify(state.currentModel));
        model.value[payload.propName] = +payload.value;
        state.currentModel = model;
    },
    UPDATE_MODEL_PROP: (state, prop) => {
        let model = JSON.parse(JSON.stringify(state.currentModel));
        if (isNumeric(prop.value)) {
            model[prop.sectionName][prop.propName] = +prop.value;
        } else {
            model[prop.sectionName][prop.propName] = prop.value;
        }

        state.currentModel = model;


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

          return axios.put(url, payload, {withCredentials: true })
              .then((response) => {
                  console.log(response);
                  // getters.settings.filter((setting) => (setting.id ===  payload.id));
              })
              .catch((err) => {
                    console.log(err)
                })
      }
  }
};

export default settingsState