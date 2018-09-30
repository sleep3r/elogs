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
                <button v-show="!config_flag" class="delete-btn" @click="deleteGraph(item.i)">Delete</button>
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
          config: null,
          message: "Loading dashboard config...",
          config_flag: true,
          draggable: true,
          resizable: true,
          dragIgnoreFrom: ".plotly, .delete-btn",
          index: 0
    }
  },
  methods: {
      layoutUpdatedEvent: function(newLayout) {
          console.log(newLayout)
          axios.post(
              "http://localhost:8000/dashboard/update-config",
              newLayout, {withCredentials: true}
          )
      },

      resizedEvent: function(i, newH, newW, newHpx, newWpx) {
          Plotly.relayout(i, {
              autosize: false,
              width: newWpx - 4,
              height: newHpx - 30,
          })
      },
      deleteGraph: function(id) {
          console.log("deleting " + id)
          axios.post(
              "http://localhost:8000/dashboard/delete-graph",
              {id: id},
              {withCredentials: true},
          )
          for (var elem in this.config) {
              console.log(id, this.config[elem].i)
              if (this.config[elem].i == id) {
                  this.config.splice(elem, 1);
                  console.log("deleted " + id)
              }
          }
      }
  },
  mounted(){
      let self = this;
      axios.get(
          'http://' + window.location.hostname + ':8000/dashboard/get-config',
          {withCredentials: true},
      ).then(function (response) {
            console.log(response.data)
            if ($.isEmptyObject(response.data.config)) {
                self.message = "There is no data"
            }
            else {
                self.config = response.data.config
                self.config_flag = false
                console.log(self)
            }
        })
  }
}
</script>

<style>
.delete-btn {
    background: solid light-grey;
}

.delete-btn:hover{
    cursor: pointer;
}

</style>
