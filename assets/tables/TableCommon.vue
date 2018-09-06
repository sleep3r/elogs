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
  methods: {},
  render: function(createElement) {
    if (!this.template) {
      return createElement('div', 'Loading...');
    } else {
      return createElement({template: "<div class=\"journal-table\" id=\"table_id_" + this.name + "\">" +
        "<div class=\"table__title\" >" + this.title + "</div>" +
              this.template + "<table-comment table-name=\"" + this.tableName + "\"></table-comment></div>",
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
              getRowsCount: function() {
                  if (this.journalInfo) {
                      let max = -1;
                      let fields = this.journalInfo.journal.tables[this.props.tableName].fields;
                      for(let field in fields) {
                        for (let index in fields[field].cells) {
                            index = parseInt(index);
                            max = max < index ? index : max
                        }
                      }
                      return max+1;
                  }
                  return -1;
              }
          },
          mounted() {
            let self = this;
            this.$root.$on('journalLoaded',function(payload) {
                self.data.rowsCount = self.getRowsCount();
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
      })
      .catch(function (error) {
        console.log('error: ', error);
      })
  },
}
</script>
