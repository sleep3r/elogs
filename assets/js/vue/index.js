import Vue from 'vue';
import Cell from './Cell.vue';
import axios from 'axios';


new Vue({
  el: '#elogs-app',
  components: { Cell },
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
      let maxCellIndex = 1
      if (this.cellgroup_info != '') {
        let fields = this.cellgroup_info.journal.tables.big.fields
        for(let field in fields) {
          for (cellIndex in fields[field].cells) {
            let cellIndex = parseInt(cellIndex)
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
