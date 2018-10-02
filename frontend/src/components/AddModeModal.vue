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
                            <input type="text" class="form-control" id="plantName" v-model="currentAddingMode.plant" placeholder="Введите название цеха">
                        </div>
                        <div class="form-group" id="journal" v-if="currentAddingMode.plant">
                            <label for="journalName">Журнал</label>
                            <input type="text" class="form-control" id="journalName" v-model="currentAddingMode.journal" placeholder="Введите название журнала">
                        </div>
                        <div class="form-group fields-container" id="fields" v-if="currentAddingMode.plant && currentAddingMode.journal">
                            <label>Поля</label>
                            <p v-if="!currentAddingMode.fields.length" class="no-fields-text">Нет полей</p>
                            <template v-else>
                                <div class="row field-item" v-for="(item, index) in currentAddingMode.fields" :key="index">
                                    <div class="col">
                                        <input type="text" class="form-control" v-model="item['table_name']" placeholder="Таблица">
                                    </div>
                                    <div class="col">
                                        <input type="text" class="form-control" v-model="item['name']" placeholder="Ячейка">
                                    </div>
                                    <div class="col">
                                        <input type="text" class="form-control" v-model="item['min_normal']" placeholder="Мин. значение">
                                    </div>
                                    <div class="col">
                                        <input type="text" class="form-control" v-model="item['max_normal']" placeholder="Макс. значение">
                                    </div>
                                    <div class="delete-icon" @click="onDeleteField(index)"><i class="fas fa-minus"></i></div>
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
    export default {
        name: "AddModeModal",
        data () {
            return {
                currentAddingMode: {
                    message: '',
                    plant: '',
                    journal: '',
                    fields: []
                }
            }
        },
        methods: {
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
                    name: '',
                    min_normal: '',
                    max_normal: ''
                })
            },
            onDeleteField (fieldIndex) {
                this.currentAddingMode.fields = this.currentAddingMode.fields.filter((item, index) => index !== fieldIndex)
            }
        }
    }
</script>

<style scoped>

</style>