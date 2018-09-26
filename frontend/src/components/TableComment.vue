<template>
    <div class="table__comment">
        <a href="javascript:;" @click="onClick">Комментарий </a>
        <i class="fas fa-envelope ico-comment"></i>
        <div :class="['comment__text', { collapse: isCollapsed }]">
          <textarea
            class="table-comment"
            @change="onChange"
            placeholder="Комментарий..."
            title=""
            v-model="text">
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
      isCollapsed: true,
      text: '',
      rowIndex: '0',
      fieldName: 'comment'
    }
  },
  methods: {
    onClick() {
      this.isCollapsed = !this.isCollapsed;
    },
    onChange() {
      axios
        .post('/common/save_cell/', {
          'cell_location': {
            'group_id': this.$store.state.journalInfo.id,
            'table_name': this.tableName,
            'field_name': this.fieldName,
            'index': this.rowIndex
          },
          'value': this.text
        })
        .then(response => {
          if (response.data.status !== 1) {
              console.log('didn`t save comment on server status:', response.data.status);
          }
        })
    },
    bindText() {
        if (this.$store.getters['journalState/journal']) {
            let cells = this.$store.getters['journalState/fieldCells'](this.tableName, this.fieldName)
            if (Object.keys(cells).length !== 0) {
                if (this.rowIndex in cells) {
                    this.text = cells[this.rowIndex].value;
                    this.isCollapsed = false
                }
            }
        }
    }
  },
  mounted() {
    this.bindText();
  }
}
</script>
