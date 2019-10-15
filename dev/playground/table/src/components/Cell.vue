<template>
  <input class="number-cell form-control general-value" type="text" name="field_name" v-model="value" />
</template>

<script>
export default {
  name: 'Cell',
  props: ['cellgroupInfo', 'tableName', 'fieldName', 'rowIndex'],
  computed: {
    value: {
      get: function () {
        // if (this.cellgroupInfo != '') {
        //   let cells = this.cellgroupInfo.journal.tables[this.tableName].fields[this.fieldName].cells
        //   if (typeof cells[this.index] !== "undefined") {
        //     return cells[this.index].value
        //   }
        // }
        return ''
      },
      set: function (value) {
        this.$emit('change_cell', this.tableName, this.fieldName, this.index, value)
      }
    }
  },
}
</script>
