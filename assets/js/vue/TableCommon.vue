<script>
import Vue from 'vue/dist/vue.esm.js'
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
      template: null
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
      return this.template();
    }
  },
  mounted() {
    let self = this;
    let templateUrl = '/templates/tables/' + this.plantName + '/' + this.journalName + '/' + this.tableName;
    console.log(templateUrl);
    axios.get(templateUrl)
      .then(function (response) {
        console.log("" + response.data)
        self.template =  Vue.compile("" + response.data).render;
      })
      .catch(function (error) {
        console.log('error!!!!!!')
        console.log(error);
      })
      .then(function () {

      });
  },
  components: {
    Cell
  }
}
</script>
