<template>
    <div class="modal fade" id="addModeModal" tabindex="-1" role="dialog" aria-labelledby="ModeModal" aria-hidden="true">
        <div class="modal-dialog modal-dialog-large" role="document">
            <div class="modal-content modal-content-large">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h5 class="modal-title"> Добавление режима </h5>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group">
                            <label for="message">Сообщение</label>
                            <input type="text" class="form-control" id="message" v-model="currentAddingMode.message" placeholder="Введите сообщение">
                        </div>
                        <div class="form-group" id="plant">
                            <label for="plantName">Цех</label>
                            <input
                                    type="text"
                                    class="form-control"
                                    id="plantName"
                                    @input="(e) => onInputChange('plant', e.target.value)"
                                    placeholder="Введите название цеха"
                                    list="plantList">
                            <datalist id="plantList">
                                <option v-for="item in plantList" :value="item.verboseName" :key="'plant-' + item.name"></option>
                            </datalist>
                        </div>
                        <div class="form-group" id="journal" v-if="currentAddingMode.plant">
                            <label for="journalName">Журнал</label>
                            <input
                                    type="text"
                                    class="form-control"
                                    id="journalName"
                                    @input="(e) => onInputChange('journal', e.target.value)"
                                    placeholder="Введите название журнала"
                                    list="journalList">
                            <datalist id="journalList">
                                <option v-for="item in journalList" :value="item.verboseName" :key="'journal-' + item.name"></option>
                            </datalist>
                        </div>
                        <div class="form-group fields-container" id="fields" v-if="currentAddingMode.plant && currentAddingMode.journal">
                            <label>Поля</label>
                            <p v-if="!currentAddingMode.fields.length" class="no-fields-text">Нет полей</p>
                            <template v-else>
                                <div class="row field-item" v-for="(item, index) in currentAddingMode.fields" :key="index">
                                    <div class="col">
                                        <input
                                                type="text"
                                                class="form-control"
                                                v-model="item.verbose_table_name"
                                                @input="(e) => onInputChange('table', e.target.value, index)"
                                                placeholder="Таблица"
                                                :list='"table-" + index'>
                                        <datalist :id='"table-" + index'>
                                            <option v-for="item in tableList" :value="item.name" :key="'table-' + item.name + '-' + index"></option>
                                        </datalist>
                                    </div>
                                    <div class="col">
                                        <input
                                                type="text"
                                                class="form-control"
                                                v-model="item.verbose_name"
                                                @input="(e) => onInputChange('field', e.target.value, index)"
                                                placeholder="Ячейка"
                                                :list='"cell-" + index'>
                                        <datalist :id='"cell-" + index' v-if="item['table_name']">
                                            <option v-for="item in fieldList" :value="item.name" :key="'field-' + item.name + '-' + index"></option>
                                        </datalist>
                                    </div>
                                    <div class="col">
                                        <input type="text" class="form-control" v-model="item['min_normal']" placeholder="Мин. значение">
                                    </div>
                                    <div class="col">
                                        <input type="text" class="form-control" v-model="item['max_normal']" placeholder="Макс. значение">
                                    </div>
                                    <div class="delete-icon" @click="onDeleteField(index)"><i class="fas fa-times"></i></div>
                                </div>
                            </template>
                        </div>
                        <div class="btns" v-if="currentAddingMode.plant && currentAddingMode.journal">
                            <button class="btn" data-target="mode-cell-add" @click.prevent="onAddField">Добавить поле</button>
                            <button class="btn" data-target="mode-add" @click.prevent="onAddMode">Сохранить</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import ajax from '../axios.config'
    import shortid from 'shortid'

    export default {
        name: "AddModeModal",
        data () {
            return {
                plantList: [],
                journalList: [],
                tableList: [],
                fieldList: [],
                randomIds: [],
                currentAddingMode: {
                    message: '',
                    plant: '',
                    journal: '',
                    fields: []
                }
            }
        },
        methods: {
            getRandomId (index) {
                return this.randomIds.filter(item => item.index === index)[0].id
            },
            onAddMode () {
                this.$store.dispatch('modesState/addMode', { mode: this.currentAddingMode })
                    .then(() => {
                        $('#addModeModal button.close').trigger('click')
                    })
                    .then(() => {
                        this.$store.dispatch('modesState/getModes')
                    })
            },
            onAddField () {
                this.currentAddingMode.fields.push({
                    table_name: '',
                    verbose_table_name: '',
                    name: '',
                    verbose_name: '',
                    min_normal: '',
                    max_normal: ''
                })

                this.tableList = []
                this.fieldList = []
            },
            onDeleteField (fieldIndex) {
                this.currentAddingMode.fields = this.currentAddingMode.fields.filter((item, index) => index !== fieldIndex)
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
            getNameByVerboseName (listType, value) {
                let currentPlant = this[listType].filter(item => item.verboseName === value)[0]
                if (currentPlant) {
                    return currentPlant.name
                }
                else {
                    return undefined
                }
            },
            onInputChange(propType, value, index) {
                if (propType === 'plant') {
                    this.getPlants()
                        .then(() => {
                            if (this.getNameByVerboseName('plantList', value)) {
                                this.currentAddingMode.plant = this.getNameByVerboseName('plantList', value)
                            }
                            else {
                                this.currentAddingMode.plant = ''
                                this.journalList = []
                                this.tableList = []
                                this.fieldList = []
                            }
                        })
                }
                else if (propType === 'journal') {
                    this.getJournals(this.currentAddingMode.plant)
                        .then(() => {
                            if (this.getNameByVerboseName('journalList', value)) {
                                this.currentAddingMode.journal = this.getNameByVerboseName('journalList', value)
                            }
                            else {
                                this.currentAddingMode.journal = ''
                                this.tableList = []
                                this.fieldList = []
                            }
                        })
                }
                else if (propType === 'table') {
                    this.getTables(this.currentAddingMode.plant, this.currentAddingMode.journal)
                        .then(() => {
                            if (this.getExistingName('tableList', value)) {
                                this.currentAddingMode.fields[index].table_name = value
                            }
                            else {
                                this.currentAddingMode.fields[index].table_name = ''
                                this.fieldList = []
                            }
                        })
                }
                else if (propType === 'field' && this.currentAddingMode.fields[index].table_name) {
                    this.getFields(this.currentAddingMode.plant, this.currentAddingMode.journal, this.currentAddingMode.fields[index].table_name)
                        .then(() => {
                            if (this.getExistingName('fieldList', value)) {
                                this.currentAddingMode.fields[index].name = value
                            }
                            else {
                                this.currentAddingMode.fields[index].name = ''
                            }
                        })
                }
            },
            getPlants () {
                return ajax.get(window.HOSTNAME + '/api/plants/',
                    {
                        withCredentials: true
                    })
                    .then(response => {
                        this.plantList = response.data.filter(item => this.$store.getters['userState/hasPerm'](`modify_${item.name}`) || this.$store.getters['userState/isSuperuser'])
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            getJournals (plant) {
                return ajax.get(window.HOSTNAME + `/api/journals/?plant=${plant}`,
                    {
                        withCredentials: true
                    })
                    .then(response => {
                        this.journalList = response.data
                    })
                    .catch(e => {
                        console.log(e)
                    })
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
        },
        mounted () {
            this.currentAddingMode.fields.map((item, index) => {
                this.randomIds.push({
                    index: index,
                    id: shortid.generate()
                })
            })
        }
    }
</script>

<style scoped>

</style>