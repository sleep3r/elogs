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
                            <label for="table_name" class="col-form-label">Таблица:</label>
                            <input type="text" class="form-control bordered" id="table_name" placeholder="Введите название таблицы">
                        </div>
                        <div class="form-group">
                            <label for="name" class="col-form-label">Ячейка:</label>
                            <input type="text" class="form-control bordered" id="name" placeholder="Введите название ячейки">
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
    export default {
        name: "AddModeCellModal",
        methods: {
            onAddCell () {
                this.$store.commit('modesState/ADD_NEW_CELL', {
                    tableName: $('input[id=table_name]').val(),
                    name: $('input[id=name]').val()
                })

                $('#AddModeCellModal button.close').trigger('click')
                this.$emit('on-add-cell')
            }
        }
    }
</script>

<style scoped>

</style>