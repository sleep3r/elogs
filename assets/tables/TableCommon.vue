<script>
    /* eslint-disable no-console */
    /* eslint no-console: "error" */

import Vue from 'vue/dist/vue.esm.js'
import axios from 'axios'
import cell from './Cell.vue'
import tableComment from './TableComment.vue'
import ToggleButton from 'vue-js-toggle-button'

Vue.use(ToggleButton);
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
      fact: false,
      template: null,
      rowsCount: 1,
      months: {
            'January': 'Январь',
            'February': 'Февраль',
            'March': 'Март',
            'April': 'Апрель',
            'May': 'Май',
            'June': 'Июнь',
            'July': 'Июль',
            'August': 'Август',
            'September': 'Сентябрь',
            'October': 'Октябрь',
            'November': 'Ноябрь',
            'December': 'Декабрь'
        },
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
            this.data.rowsCount = this.$store.getters.maxRowIndex(this.props.name) + 1;
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
    let templateUrl = '/static/templates/tables/' + this.$store.getters.plantName + '/' + this.$store.getters.journalName + '/' + this.name + ".html";
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
