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
    cellgroupInfo: Object,
    plantName: String,
    journalName: String,
    tableName: String,
    title: String
  },
  data: function() {
    return {
      template: null,
    }
  },
  computed: {
    name: function () {
      return this.tableName;
    }
  },
  methods: {
    onCellChange: function () {
      console.log('in TableCommon onCellChange ')
    }
  },
  render: function(createElement) {
    if (!this.template) {
      return createElement('div', 'Loading...');
    } else {
      return createElement({template: "<div class=\"journal-table\" id=\"table_id_table_name\">" +
        "<div class=\"table__title\" >" + this.title + "</div>" +
              this.template + "<table-comment></table-comment></div>",
        data: () => { return {
              data: this.$data,
              props: this.$props
            }
        },
        components: { 'cell': cell, 'table-comment': tableComment }
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
  components: {
    'cell': cell
  }
}
</script>
