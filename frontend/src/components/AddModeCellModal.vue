<template>
    <div class="modal fade" id="AddModeCellModal" tabindex="-1" role="dialog" aria-labelledby="AddModeCellModal" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h5 class="modal-title"> Добавление ячейки </h5>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group">
                            <label for="table_name" class="col-form-label">Таблица</label>
                            <input
                                    type="text"
                                    class="form-control bordered"
                                    id="table_name"
                                    placeholder="Введите название таблицы"
                                    @input="(e) => onInputChange('table', e.target.value)"
                                    list="table"
                            >
                            <datalist id="table">
                                <option v-for="item in tableList" :value="item.name" :key="'table-' + item.name"></option>
                            </datalist>
                        </div>
                        <div class="form-group">
                            <label for="name" class="col-form-label">Столбец</label>
                            <input
                                    type="text"
                                    class="form-control bordered"
                                    id="name"
                                    placeholder="Введите название ячейки"
                                    @input="(e) => onInputChange('field', e.target.value)"
                                    list="field"
                            >
                            <datalist id="field" v-if="table_name">
                                <option v-for="item in fieldList" :value="item.name" :key="'field-' + item.name + '-' + index"></option>
                            </datalist>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn" data-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn" @click.prevent="onAddCell">Добавить</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    import ajax from '../axios.config'

    export default {
        name: "AddModeCellModal",
        data () {
            return {
                table_name: '',
                name: '',
                tableList: [],
                fieldList: []
            }
        },
        computed: {
            getCurrentPlant () {
                return Object.keys(this.$store.getters['modesState/currentMode'].plant)[0]
            },
            getCurrentJournal () {
                return Object.keys(this.$store.getters['modesState/currentMode'].journal)[0]
            }
        },
        methods: {
            onAddCell () {
                this.$store.commit('modesState/ADD_NEW_CELL', {
                    tableName: $('input[id=table_name]').val(),
                    name: $('input[id=name]').val()
                })

                $('#AddModeCellModal button.close').trigger('click')
                this.$emit('on-add-cell')
            },
            getExistingName (listType, value) {
                let currentItem = this[listType].filter(item => item.name === value)[0]
                if (currentItem) {
                    return currentItem.name
                }
                else {
                    return undefined
                }
            },
            onInputChange(propType, value, index) {
                if (propType === 'table') {
                    console.log(this.getCurrentPlant, this.getCurrentJournal)
                    this.getTables(this.getCurrentPlant, this.getCurrentJournal)
                        .then(() => {
                            if (this.getExistingName('tableList', value)) {
                                this.table_name = value
                            }
                            else {
                                this.table_name = ''
                                this.fieldList = []
                            }
                        })
                }
                else if (propType === 'field' && this.table_name) {
                    this.getFields(this.getCurrentPlant, this.getCurrentJournal, this.table_name)
                        .then(() => {
                            if (this.getExistingName('fieldList', value)) {
                                this.name = value
                            }
                            else {
                                this.name = ''
                            }
                        })
                }
            },
            getTables (plant, journal) {
                return ajax.get(window.HOSTNAME + `/api/tables/?plant=${plant}&journal=${journal}`,
                    {
                        withCredentials: true
                    })
                    .then(response => {
                        this.tableList = response.data
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            getFields (plant, journal, table) {
                return ajax.get(window.HOSTNAME + `/api/fields/?plant=${plant}&journal=${journal}&table=${table}`,
                    {
                        withCredentials: true
                    })
                    .then(response => {
                        this.fieldList = response.data
                    })
                    .catch(e => {
                        console.log(e)
                    })
            }
        }
    }
</script>

<style scoped>

</style>