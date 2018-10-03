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
                <div class="mode-content__title__mode-btns" v-if="!editMode">
                    <button class="btn" v-if="currentMode.is_active" value="off" @click.prevent="toggleMode(0)">Выключить</button>
                    <button class="btn" v-else value="on" @click.prevent="toggleMode(1)">Включить</button>
                    <button class="btn" data-target="mode-edit" @click.prevent="onEditModeChange">Изменить</button>
                    <button class="btn" data-target="mode-delete" @click.prevent="onDeleteMode">Удалить</button>
                </div>
                <div class="mode-content__title__mode-edit-btns" v-else>
                    <button class="btn" data-target="mode-add-row" @click.prevent="onAddRow">Добавить ячейку</button>
                    <button class="btn" data-target="mode-save" @click.prevent="onSaveMode">Сохранить</button>
                </div>
            </template>
        </div>
        <div class="mode-content__body">
            <table class="table table-bordered elog-journal-table" v-if="currentMode">
                <thead>
                    <tr>
                        <th>Таблица</th>
                        <th>Ячейка</th>
                        <th>Минимальное значение</th>
                        <th>Максимальное значение</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in currentMode.fields">
                        <td data-target="table_name"><div>{{item.table_name}}</div></td>
                        <td data-target="name"><div>{{item.name}}</div></td>
                        <td data-target="min_normal"><div>{{item.min_normal}}</div></td>
                        <td data-target="max_normal"><div>{{item.max_normal}}</div></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ModesPage",
        data () {
            return {
                editMode: false,
                modeFields: []
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
            onEditModeChange () {
                $('.mode-content__body td').each(function () {
                    $(this).html($(`<input type="text" class="form-control" value="${$(this).text()}">`))
                })

                this.editMode = true
            },
            onSaveMode () {
                $('.mode-content__body tbody tr').each(function () {
                    let _this = this
                    $(this).children('td').each(function () {
                        if (!$(this).find('input').val()) {
                            $(_this).remove()
                        }
                    })
                })
                $('.mode-content__body td').each(function () {
                    $(this).html(`<div>${$(this).find('input').val()}</div>`)
                })

                this.$store.dispatch('modesState/updateMode', {...this.currentMode, fields: this.getUpdatedFieldItems()})
                    .then(() => {
                        this.$store.dispatch('modesState/getModes')
                            .then(() => {
                                this.currentMode = null
                                // this.currentMode = this.getURLParameter('modeId')
                            })
                    })
                this.editMode = false
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
            onAddRow () {
                let updatedFields = this.currentMode.fields
                updatedFields.push({
                    table_name: '',
                    name: '',
                    min_normal: '',
                    max_normal: ''
                })

                this.$store.commit('modesState/UPDATE_CURRENT_MODE', {...this.currentMode, fields: updatedFields})

                setTimeout(() => {
                    $('.mode-content__body td').each(function () {
                        if (!$(this).has('input').length) {
                            $(this).html($(`<input type="text" class="form-control" value="${$(this).text()}">`))
                        }
                    })
                }, 0)
            },
            getUpdatedFieldItems () {
                let updatedFields = []
                $('.mode-content__body tbody tr').each(function () {
                    updatedFields.push({
                        table_name: $(this).children('td[data-target="table_name"]').find('div').text(),
                        name: $(this).children('td[data-target="name"]').find('div').text(),
                        min_normal: +$(this).children('td[data-target="min_normal"]').find('div').text(),
                        max_normal: +$(this).children('td[data-target="max_normal"]').find('div').text()
                    })
                })
                return updatedFields
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
    .mode-content table {
        table-layout: fixed !important;
    }

    .mode-content table td div {
        padding: 0.375rem 3px !important;
    }

    .mode-content table .form-control {
        border-radius: 0;
        padding-left: 3px;
        padding-right: 3px;
    }
</style>
