<script>
    /* eslint-disable no-console */
    /* eslint no-console: "error" */

import axios from 'axios'
import Cell from './Cell.vue'

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
        components: { Cell }
      })
    }
  },
  mounted() {
    let self = this;
    let templateUrl = '/templates/tables/' + this.plantName + '/' + this.journalName + '/' + this.tableName + ".html";
    console.info(templateUrl);
    axios.get(templateUrl)
      .then(function (response) {
         self.template = response.data;
      })
      .catch(function (error) {
        console.log('error: ', error);
      })
  },
  components: {
    Cell
  }
}
</script>
