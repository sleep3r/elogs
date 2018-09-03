<script>
    /* eslint-disable no-console */
    /* eslint no-console: "error" */

import Vue from 'vue/dist/vue.esm.js'
import axios from 'axios'
import cell from './Cell.vue'

Vue.component('cell', cell);
Vue.component('Cell', cell);

export default {
  name: 'TableCommon',
  props: {
    cellgroupInfo: Object,
    plantName: String,
    journalName: String,
    tableName: String,
  },
  data: function() {
    return {
      template: null,
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
      return createElement({template: this.template,
        props: this.$props,
        data: () => this.$data,
        components: { 'cell': cell }
      })
    }
  },
  mounted() {
    let self = this;
    let templateUrl = '/static/templates/tables/' + this.plantName + '/' + this.journalName + '/' + this.tableName + ".html";
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
