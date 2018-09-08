<template>
  <input :class="classes"
         type="text"
         :name="fieldName"
         :row-index="rowIndex"
         :value="value"
         @change="onChanged"
         @input="onInput"
  />
</template>

<script>
import axios from 'axios'

export default {
  name: 'Cell',
  props: [
      'fieldName',
      'rowIndex',
      'linked'
  ],
  data() {
    return {
        classes: 'general-value number-cell form-control',
        value: '',
    }
  },
  computed: {
    tableName: function() {
        if (typeof this.$parent.props !== 'undefined') {
          return this.$parent.props.name;
        }
        else {
          return ''
        }
    }
  },
  methods: {
      send() {
        axios
          .post('/common/save_cell/', {
            'cell_location': {
              'group_id': this.$store.state.journalInfo.id,
              'table_name': this.tableName,
              'field_name': this.fieldName,
              'index': this.rowIndex
            },
            'value': this.value
          })
          .then(response => {
            if (response.data.status !== 1) {
              console.log('didn`t save cell on server status:', response.data.status);
            }
          })
      },
      onInput(e) {
        this.value = e.target.value
        this.$store.commit('SAVE_CELL_VALUE', {
          tableName: this.tableName,
          fieldName: this.fieldName,
          index: this.rowIndex,
          value: this.value
        })
        this.$parent.$emit('addNewLine', { editedRowIndex: this.rowIndex });
      },
      onChanged() {
        this.send();
      },
  },
  mounted() {
    this.value = this.$store.getters.cellValue(this.tableName, this.fieldName, this.rowIndex)
    if (this.linked) {
      this.value = this.$store.getters[this.linked];
      this.send();
    }
  }
}
</script>
