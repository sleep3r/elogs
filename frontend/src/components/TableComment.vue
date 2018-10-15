<template>
    <div class="table__comment">
        <div v-if="mode==='edit'">
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
        <div v-else>
          Комментарий: {{ text }}
        </div>
    </div>
</template>

<script>

    export default {
        name: 'table-comment',
        props: [ 'tableName' ],
        data() {
            return {
                rowIndex: '0',
                isCollapsed: true,
                fieldName: '__table__comment'
            }
        },
        watch: {
            text (value) {
                this.isCollapsed = value ? false : true
            }
        },
        computed: {
            mode() {
                return this.$store.state.journalState.journalInfo.mode;
            },
            text: {
                get: function () {
                    return this.$store.getters['journalState/cell'](this.tableName, this.fieldName, this.rowIndex)['value']
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
