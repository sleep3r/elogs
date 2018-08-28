<template>
  <input class="number-cell form-control general-value" type="text" name="field_name" v-model="value" />
</template>

<script>
import axios from 'axios';

export default {
  props: ['cellgroup_info', 'table_name', 'field_name', 'index'],
  computed: {
    value: {
      get: function () {
        if (this.cellgroup_info != '') {
          let cells = this.cellgroup_info.journal.tables[this.table_name].fields[this.field_name].cells
          if (typeof cells[this.index] !== "undefined") {
            return cells[this.index].value
          }
        }
        return ''
      },
      set: function (value) {
        this.saveCell(value)
      }
    }
  },
  methods: {
    saveCell: function (value) {
      axios
        .post('/common/save_cell/', {
          'cell_location': {
            'group_id': this.cellgroup_info.id,
            'table_name': this.table_name,
            'field_name': this.field_name,
            'index': this.index
          },
          'value': value
        })
        .then(response => {
          this.$emit('change_cell')
        })
    }
  },
  template: ''
}
</script>
