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
    name: String,
  },
  data: function () {
    return {
      template: null,
      rowsCount: 1
    }
  },
  render: function (createElement) {
    if (!this.template) {
      return createElement('div', 'Loading...');
    } else {
      return createElement({template: "<div class=\"journal-table\" id=\"table_id_" + this.name + "\">" +
              this.template + "<table-comment table-name=\"" + this.name + "\"></table-comment></div>",
          name: 'table-' + this.name,
          data: () => { return {
              data: this.$data,
              props: this.$props
          }},
          components: { 'cell': cell, 'table-comment': tableComment },
          mounted() {
            let self = this;
            this.data.rowsCount = this.$store.getters['journalState/maxRowIndex'](this.props.name) + 1;
            this.$on('addNewLine', function (payload) {
                if (self.data.rowsCount - 1  === payload.editedRowIndex) {
                    self.data.rowsCount += 1;
                }
            });
          }
      })
    }
  },
  mounted() {
    let self = this;
    let templateUrl = 'http://localhost:8000/templates/tables/' + this.$store.getters['journalState/plantName'] + '/' + this.$store.getters['journalState/journalName'] + '/' + this.name;
    axios.get(templateUrl, {withCredentials: true})
      .then(function (response) {
         self.template = response.data;
      })
      .catch(function (error) {
        console.log('error: ', error);
      })
  },
}
</script>
