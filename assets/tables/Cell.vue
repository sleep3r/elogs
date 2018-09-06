<template>
  <input :class="classes"
         type="text"
         v-bind:name="fieldName"
         v-bind:row-index="rowIndex"
         v-model="value"
         v-on:change="onChanged"
         v-on:input="onInput"
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
        value: '',
        classes: 'general-value number-cell form-control'
    }
  },
  computed: {
    tableName: function() {
        return this.$parent.props.tableName;
    },
    journalInfo: function() {
        if (!this.$root.journalInfo) {
            return null;
        }
        return this.$root.journalInfo;
    },
  },
  methods: {
      send(){
          axios
            .post('/common/save_cell/', {
              'cell_location': {
                'group_id': this.journalInfo.id,
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
      onInput() {
            this.$parent.$emit('addNewLine', { editedRowNumber: this.rowIndex });
      },
      onChanged() {
          this.send();
      },
      bindValue() {
          if (!("journal" in this.journalInfo) === false ) {
            let cells = this.journalInfo.journal.tables[this.tableName].fields[this.fieldName].cells;
            if (Object.keys(cells).length !== 0) {
                if (this.rowIndex in cells) {
                    this.value = cells[this.rowIndex].value;
                }
            }
            this.value = this.$store.getters[this.linked]
          }

      }

  },
  mounted() {
      this.bindValue();
    }
}
</script>
