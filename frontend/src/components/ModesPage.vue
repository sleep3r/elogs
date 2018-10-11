<template>
    <div class="mode-content">
        <div class="mode-content__title">
            <div class="mode-content__title__mode-info">
                <h3 id="modeTitle">
                    <span v-if="!currentMode">Выберите режим</span>
                    <span v-else>{{currentMode.message}}</span>
                </h3>
            </div>
            <template v-if="currentMode">
                <div class="mode-content__title__mode-btns">
                    <button class="btn" v-if="currentMode.is_active" value="off" @click.prevent="toggleMode(0)">Выключить</button>
                    <button class="btn" v-else value="on" @click.prevent="toggleMode(1)">Включить</button>
                    <button class="btn" data-target="mode-delete" @click.prevent="onDeleteMode">Удалить</button>
                </div>
            </template>
        </div>
        <div class="mode-content__body">
            <div class="table-container">
                <table class="table table-bordered elog-journal-table" v-if="currentMode">
                    <thead>
                    <tr>
                        <th>Таблица</th>
                        <th>Ячейка</th>
                        <th>Минимальное значение</th>
                        <th>Максимальное значение</th>
                        <th style="width: 36px"></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(item, index) in currentMode.fields" :key="item.name + '-' + index">
                        <td data-target="table_name"><div>{{item.table_name}}</div></td>
                        <td data-target="name"><div>{{item.name}}</div></td>
                        <td data-target="min_normal">
                            <input
                                    type="number"
                                    class="form-control"
                                    :value="item.min_normal"
                                    @input="(e) => onChangeCellValue('min_normal', item.table_name, item.name, e.target.value)"
                            >
                        </td>
                        <td data-target="max_normal">
                            <input
                                    type="number"
                                    class="form-control"
                                    :value="item.max_normal"
                                    @input="(e) => onChangeCellValue('max_normal', item.table_name, item.name, e.target.value)"
                            >
                        </td>
                        <td>
                            <div class="delete-icon" @click="onDeleteCell(item.table_name, item.name)"><i class="fas fa-times"></i></div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            <div class="mode-content__title__mode-edit-btns" v-if="currentMode">
                <button class="btn" data-toggle="modal" data-target="#AddModeCellModal">Добавить ячейку</button>
                <div v-if="needsToSave">
                    <button class="btn" data-target="mode-cancel" @click.prevent="onCancelMode" style="margin-right: 10px">Отмена</button>
                    <button class="btn" data-target="mode-save" @click.prevent="onSaveMode">Сохранить</button>
                </div>
            </div>
        </div>
        <add-mode-cell-modal @on-add-cell="needsToSave = true"></add-mode-cell-modal>
    </div>
</template>

<script>
    import AddModeCellModal from './AddModeCellModal.vue'

    export default {
        name: "ModesPage",
        components: {
            'add-mode-cell-modal': AddModeCellModal
        },
        data () {
            return {
                needsToSave: false
            }
        },
        computed: {
            currentMode: {
                get () {
                    return this.$store.getters['modesState/currentMode']
                },
                set (value) {
                    this.$store.commit('modesState/SET_CURRENT_MODE', value)
                }
            }
        },
        methods: {
            onDeleteCell (tableName, name) {
                this.$store.commit('modesState/DELETE_CELL', {
                    tableName,
                    name
                })

                this.needsToSave = true
            },
            onCancelMode () {
                this.$store.commit('modesState/CANCEL_MODE', this.getURLParameter('modeId'))

                this.needsToSave = false
            },
            onSaveMode () {
                this.$store.dispatch('modesState/updateMode', this.currentMode)
                    .then(() => {
                        this.$store.dispatch('modesState/getModes')
                            .then(() => {
                                this.currentMode = this.getURLParameter('modeId')
                            })
                    })
                this.needsToSave = false
            },
            onChangeCellValue (dataType, tableName, name, value) {
                this.$store.commit('modesState/CHANGE_CELL_VALUE', {
                    dataType,
                    tableName,
                    name,
                    value
                })

                this.needsToSave = true
            },
            toggleMode (isActive) {
                this.$store.dispatch('modesState/toggleMode', {modeId: this.currentMode.id, isActive})
                    .then(() => {
                        this.$store.dispatch('modesState/getModes')
                            .then(() => {
                                this.currentMode = this.getURLParameter('modeId')
                            })
                    })
            },
            onDeleteMode () {
                this.$store.dispatch('modesState/deleteMode', {modeId: this.currentMode.id})
                    .then(() => {
                        this.currentMode = null
                        this.$router.push('/modes')
                    })
                    .then(() => {
                        this.$store.dispatch('modesState/getModes')
                    })
            },
            getURLParameter (paramName) {
                let url = window.location.search.substring(1);
                let urlParams = url.split('&');
                for (let i = 0; i < urlParams.length; i++) {
                    let parameterName = urlParams[i].split('=');
                    if (parameterName[0] === paramName) {
                        return parameterName[1];
                    }
                }
                return "";
            }
        },
        destroyed () {
            this.currentMode = null
        },
        mounted () {
            this.$store.dispatch('modesState/getModes')
                .then(() => {
                    if (this.getURLParameter('modeId')) {
                        this.currentMode = this.getURLParameter('modeId')
                    }
                    else {
                        this.currentMode = null
                    }
                })
        }
    }
</script>

<style>

</style>
