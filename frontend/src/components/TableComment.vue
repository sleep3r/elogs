<template>
    <div class="table__comment">
        <a href="javascript:;" @click="onClick">Комментарий </a>
        <i class="fas fa-envelope ico-comment"></i>
        <div :class="['comment__text', { collapse: isCollapsed }]">
          <textarea
                  class="table-comment"
                  placeholder="Комментарий..."
                  title=""
                  :value="text"
                  @input="onInput">
          </textarea>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'table-comment',
        props: [ 'tableName' ],
        data() {
            return {
                rowIndex: '-1',
                isCollapsed: true,
                fieldName: '__table__comment'
            }
        },
        computed: {
            text: {
                get: function () {
                    return this.text = this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)['value']
                },
                set: function (val) {
                    this.$store.commit('journalState/SAVE_CELLS', {'cells': [{
                        tableName: this.tableName,
                        fieldName: this.fieldName,
                        index: this.rowIndex,
                        value: val,
                    }]});
                }
            }
        },
        methods: {
            onInput(e) {
                this.text = e.target.value
                this.send()
            },
            onClick() {
                this.isCollapsed = !this.isCollapsed;
            },
            send() {
                this.$socket.sendObj({
                    'type': 'shift_data',
                    'cells': [{
                        'cell_location': {
                            'group_id': this.$store.getters['journalState/journalInfo'].id,
                            'table_name': this.tableName,
                            'field_name': this.fieldName,
                            'index': this.rowIndex
                        },
                        'value': this.text || ''
                    }]
                });
            }
        },
        mounted() {
            if (this.text) {
                this.isCollapsed = false;
            }
        }
    }
</script>
