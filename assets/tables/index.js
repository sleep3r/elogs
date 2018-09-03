import Vue from 'vue/dist/vue.esm.js'
import TableCommon from './TableCommon.vue';
import axios from 'axios';


Vue.component('tablecommon', TableCommon);

window.App = new Vue({
  el: '#elogs-app',
  components: { TableCommon },
  data: function () {
    return {
      pageId: '',
      plantName: '',
      journalName: '',
      cellgroupInfo: {},
        tableName: '',
      syncronized: false,
    }
  },
  delimiters: ['%{', '}'],
  computed: {
    tables: function () {
        return ['big']
    }
  },
  methods: {
    getCellGroupInfo: function () {
      this.syncronized = false
      axios
        .get('/api/shifts/' + this.pageId)
        .then(response => {
          this.syncronized = true
          this.cellgroupInfo = response.data
        })
    },
    sendCell: function (tableName, fieldName, index, value) {
      // save cell on server
      axios
        .post('/common/save_cell/', {
          'cell_location': {
            'group_id': this.cellgroupInfo.id,
            'table_name': tableName,
            'field_name': fieldName,
            'index': index
          },
          'value': value
        })
        .then(response => {
          if (response.data.status != '1') {
            console.log('DID NOT SAVE CELL ON SERVER')
          }
        })
    },
    saveCell: function (tableName, fieldName, index, value) {
      // save cell locally
      let cellInfo = {
          "value": value,
          "index": index
      }
      this.cellgroupInfo.journal.tables[tableName].fields[fieldName].cells[index] = cellInfo
      this.$forceUpdate()
    },
    onCellChange: function (tableName, fieldName, index, value) {
      this.saveCell(tableName, fieldName, index, value)
      this.sendCell(tableName, fieldName, index, value)
    }
  },
  mounted () {
    console.log('Tables were mounted')
    this.plantName = window.location.pathname.split("/")[1];
    this.journalName = window.location.pathname.split("/")[2];
    this.pageId = window.location.pathname.split("/")[3];
    this.getCellGroupInfo();
  }
});
