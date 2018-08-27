
Vue.component('cell', {
  props: ['cellgroup_info', 'table_name', 'field_name', 'index'],
  computed: {
    value: {
      get: function () {
        if (this.cellgroup_info != '') {
          cells = this.cellgroup_info.journal.tables[this.table_name].fields[this.field_name].cells
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
  template: '<input class="number-cell form-control general-value" type="text" name="field_name" v-model="value" />'
})

var elogsApp = new Vue({
  el: '#elogs-app',
  data: function () {
    return {
      plant_name: '',
      journal_name: '',
      cellgroup_info: '',
      syncronized: true,
    }
  },
  delimiters: ['%{', '}'],
  computed: {
    number_of_lines: function () {
      maxCellIndex = 1
      if (this.cellgroup_info != '') {
        fields = this.cellgroup_info.journal.tables.big.fields
        for(field in fields) {
          for (cellIndex in fields[field].cells) {
            cellIndex = parseInt(cellIndex)
            maxCellIndex = maxCellIndex < cellIndex ? cellIndex : maxCellIndex
          }
        }
      }
      return maxCellIndex+1
    }
  },
  methods: {
    getCellGroupInfo: function () {
      this.syncronized = false
      axios
        .get('/api/shifts/' + this.page_id)
        .then(response => {
          this.syncronized = true
          this.cellgroup_info = response.data
        })
    }
  },
  mounted () {
    this.plant_name = window.location.pathname.split("/")[1];
    this.journal_name = window.location.pathname.split("/")[2];
    this.page_id = window.location.pathname.split("/")[3];
    this.getCellGroupInfo();
  }
});
