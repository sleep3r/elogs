<template>
    <div class="settings">
        <!--<div class="settings-stats">-->
            <!--<b>Кол-во настроек:<span>{{countSettings}}</span></b>-->
        <!--</div>-->
        <!--<div class="search">-->
            <!--<label for="settting-search">Найти: </label>-->
            <!--<input type="text" v-model="searchByName" id="settting-search"/>-->
            <!--<button @click="uncheckAllSettings()"><i class="material-icons">check_box</i></button>-->
        <!--</div>-->
        <modal v-show="isEditing" @close="closeModal" :action="customAction" >
            <div class="panel panel-info">
                <div class="panel-heading">
                    <h3 class="panel-title">Окно редактирования setting'a</h3>
                </div>
                <div class="panel-body">
                    <setting-edit v-if="currentModel" :model="currentModel"></setting-edit>
                </div>
            </div>
        </modal>
        <div class="table-container">
            <table class="settings-list table table-striped">
                <thead>
                <tr>
                    <th>#</th>
                    <th>Type</th>
                    <th>Name</th>
                    <th>Value</th>
                    <th>User</th>
                    <th>Scope</th>
                </tr>
                </thead>
                <tbody>
                <setting-item v-for="item in filtredByName" :key="item.id" :model="item"></setting-item>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
    import SettingItem from './SettingItem.vue';
    import Modal from "../Modal.vue";
    import SettingEdit from "./settings/SettingEdit.vue";

    export default {
        name: "SettingsList",
        data() {
          return {
              isEditing: false
          }
        },
        computed: {
          customAction: function() {
            let self = this;
            return {
                callback: self.saveCurrentSetting,
                title: "Сохранить"
            }
          },
          currentModel: function() {
            return this.$store.getters['settingsState/currentModel'];
          },
          settings: function() {
              return this.$store.getters['settingsState/getSettings'];
          },
          filtredByName: function () {
            return this.$store.getters['settingsState/filtredByName'];
          },
          countSettings: function() {
            return this.filtredByName.length;
          },
          searchByName: {
                get() {
                    return this.$store.getters['settingsState/searchByName'];
                },
                set( value ) {
                    this.$store.commit('settingsState/SET_SEARCH_BY_NAME', value);
                }
            }
        },
        methods: {
            closeModal() {
                this.isEditing = false;
                this.$store.commit('settingsState/SET_CURRENT_MODEL', null);
            },
            saveCurrentSetting() {
              let model = this.currentModel;
              this.$store.dispatch('settingsState/updateSetting', model)
                  .then((model) => {
                        console.log("current model", model);
                        this.isEditing = false;
                        this.$store.commit('settingsState/SET_CURRENT_MODEL', null);
                  });

            },
            uncheckAllSettings() {
                let settings = this.$store.getters.getSettings;
                for (let set of settings) {
                    set.isFavorite = false;
                }
                this.$store.commit('settingsState/SET_SETTINGS', settings);
            },
            loadSettingsFromAPI() {
                this.$store.dispatch('settingsState/loadSettings')
                    .then(() => {
                        console.log('load settings');
                        // this.$store.dispatch('journalState/loadShifts', { plant: this.$route.params.plant, journal: this.$route.params.journal })
                    });
            }
        },
        mounted() {
            this.loadSettingsFromAPI();
        },
        components: {
            SettingEdit,
            Modal,
            SettingItem
        }
    }
</script>
<style  lang="scss">
    $color-border: #548CB7;
    .settings {
        border: 1px solid $color-border;
        padding: 10px;

        .search {
            text-align: left;
        }

        .settings-stats {
            text-align: left;
        }
    }

    .panel-body {
        text-align: left;
    }

    .settings-list {
        border: 1px solid $color-border;
        padding: 10px;
        min-height: 300px;
        list-style: none;
        text-align: left;
        height:400px;
        table-layout: auto;

        td {
            padding: 10px;
        }

        td:first-child, th:first-child {
            max-width: 30px;
        }

        li {
            font-size: 10px;
            margin-bottom: 10px;
            padding-left: 10px;

            border: 1px solid $color-border;
        }

        code {
            word-break: normal;
        }
    }

    .table-container {
        overflow-x: auto;
    }
</style>