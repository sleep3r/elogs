<template>
  <input :class="classes"
         type="text"
         v-bind:name="fieldName"
         v-bind:row-index="rowIndex"
         v-model="value"
         v-on:change="onChanged"
  />
</template>
<script>
import axios from 'axios'

export default {
  name: 'Cell',
  props: [
      'fieldName',
      'rowIndex',
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
          console.log("cell->send()", this.journalInfo);
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
              if (response.data.status != '1') {
                  console.log('DID NOT SAVE CELL ON SERVER')
              }
            })
      },
      onChanged() {
          this.send();
          console.info("table-name:", this.tableName,
              "field-name:", this.fieldName,
              "row-index:", this.rowIndex,
              "value:", this.value);
      }
  },
  mounted() {
      console.log(this.journalInfo.journal);

          console.log(this.journalInfo.journal.tables[this.tableName].fields[this.fieldName].cells);
          let obj = this.journalInfo.journal.tables[this.tableName].fields[this.fieldName].cells;
          if (Object.keys(obj).length !== 0 ) {
              this.value = this.journalInfo.journal.tables[this.tableName].fields[this.fieldName].cells[0].value;
          }

  }
}
</script>
