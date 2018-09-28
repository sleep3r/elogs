<template>
    <div :class="classes">
        <span v-if="config_flag"> {{ message }} </span>
        <grid-layout v-else
                     :layout="config"
                     :col-num="12"
                     :row-height="30"
                     :is-draggable="draggable"
                     :is-resizable="resizable"
                     :vertical-compact="true"
                     :use-css-transforms="true"
                     @layout-updated="layoutUpdatedEvent"
        >
            <grid-item v-for="item in config"
                       :x="item.x"
                       :y="item.y"
                       :w="item.w"
                       :h="item.h"
                       :i="item.i"
                       :key="item.i"
                       :id="'vue-grid-item-' + item.i"
                       :drag-ignore-from="dragIgnoreFrom"
                       @resized="resizedEvent"
                    >
                <Graph :idx="item.i"></Graph>
            </grid-item>
        </grid-layout>
    </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
import VueGridLayout from 'vue-grid-layout';
import Graph from './Graph.vue'
import Plotly from 'plotly.js-dist'

var GridLayout = VueGridLayout.GridLayout;
var GridItem = VueGridLayout.GridItem;

export default {
    name: 'Dashboard',
    components: {
        "GridLayout": GridLayout,
        "GridItem": GridItem,
        "Graph": Graph,
    },
  data() {
      return {
          classes: 'dashboard',
          config: {},
          message: "Loading dashboard config...",
          config_flag: true,
          draggable: true,
          resizable: true,
          dragIgnoreFrom: ".plotly",
          index: 0
    }
  },
  methods: {
      layoutUpdatedEvent: function(newLayout) {
          axios.post("http://localhost:8000/dashboard/update-config", newLayout)
      },

      resizedEvent: function(i, newH, newW, newHpx, newWpx) {
          Plotly.relayout(i, {
              autosize: false,
              width: newWpx - 4,
              height: newHpx - 50,
          })
      },
  },
  mounted(){
      let self = this;
      axios.get("http://localhost:8000/dashboard/get-config")
        .then(function (response) {
            console.log(response.data)
            if ($.isEmptyObject(response.data.config)) {
                self.message = "There is no data"
            }
            else {
                self.config = response.data.config
                self.config_flag = false
            }
        })
  }
}
</script>
