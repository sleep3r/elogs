<script>
    /* eslint-disable no-console */
    /* eslint no-console: "error" */

import Vue from 'vue/dist/vue.esm.js'
import axios from 'axios'
import cell from './Cell.vue'
import tableComment from './TableComment.vue'

Vue.component('cell', cell);
Vue.component('Cell', cell);
Vue.component('table-comment', tableComment);


export default {
  name: 'TableCommon',
  props: {
    plantName: String,
    journalName: String,
    tableName: String,
    title: String
  },
  data: function() {
    return {
      template: null,
      rowsCount: 0
    }
  },
  computed: {
    name: function () {
      return this.tableName;
    },
  },
  methods: {
  },
  render: function(createElement) {
    if (!this.template) {
      return createElement('div', 'Loading...');
    } else {
      return createElement({template: "<div class=\"journal-table\" id=\"table_id_" + this.name + "\">" +
        "<div class=\"table__title\" >" + this.title + "</div>" +
              this.template + "<table-comment></table-comment></div>",
          name: 'table-' + this.name,
          data: () => { return {
              data: this.$data,
              props: this.$props
          }},
          computed: {
            journalInfo: function() {
                return this.$root.journalInfo;
            }
          },
          components: { 'cell': cell, 'table-comment': tableComment },
          methods: {
              getRowsIndexies: function() {
                if (this.journalInfo) {
                    let indexies = [];
                    for (let i=0; i <= this.data.rowsCount; i++) {
                        indexies.push(i);
                    }
                    return indexies;
                } else {
                    return [];
                }
              },
              calcRows: function() {
                  let maxCellIndex = -1;
                  if (this.journalInfo) {
                    let fields = this.journalInfo.journal.tables[this.props.tableName].fields;
                    for(let field in fields) {
                      for (let cellIndex in fields[field].cells) {
                        cellIndex = parseInt(cellIndex);
                        maxCellIndex = maxCellIndex < cellIndex ? cellIndex : maxCellIndex
                      }
                    }
                    return maxCellIndex+1;
                  }
                  return maxCellIndex;
              }
          },
          mounted() {
            console.log("mounted: ", this.props.tableName);
            let self = this;
            this.$root.$on('journalLoaded',function(payload) {
                self.data.rowsCount = self.calcRows();
            });

            this.$on('addNewLine', function(payload){
                if (self.data.rowsCount === payload.editedRowNumber ) {
                    self.data.rowsCount += 1;
                }
            });
          }
      })
    }
  },
  mounted() {
    let self = this;
    let templateUrl = '/static/templates/tables/' + this.plantName + '/' + this.journalName + '/' + this.name + ".html";
    axios.get(templateUrl)
      .then(function (response) {
         self.template = response.data;
         console.log(this.journalInfo);
      })
      .catch(function (error) {
        console.log('error: ', error);
      })
  },
  components: {
    'cell': cell
  }
}
</script>
