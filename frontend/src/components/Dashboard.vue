<template>
    <div :class="classes">
        <span v-if="config_flag"> {{ message }} </span>
        <grid-layout v-else
                     :layout="layout"
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
                <Graph :idx="item.i" :type="item.type"></Graph>
                <button v-show="!config_flag" class="delete-btn" @click="deleteGraph(item.i)">Delete</button>
            </grid-item>
        </grid-layout>
    </div>
</template>

<script>
import ajax from '../axios.config'
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
  computed: {
      layout: function() {
          return Object.values(this.config)
      }
  },
  methods: {
      layoutUpdatedEvent: function(newLayout) {
          console.log(newLayout)
          ajax.post(
              window.HOSTNAME+"/dashboard/update-config",
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
          ajax.post(
              window.HOSTNAME+"/dashboard/delete-graph",
              {id: id},
              {withCredentials: true},
          )
          Vue.delete(this.config, id);
          if ($.isEmptyObject(this.config)) {
              this.message = "There is no data"
              this.config_flag = true
          }
      }
  },
  mounted(){
      let self = this;
      // this.$store.commit("UPDATE_JOURNAL_INFO", {plant: {name: "Панель аналитики"}})
      // console.log(this.$store)
      ajax.get(
          window.HOSTNAME + '/dashboard/get-config',
          {withCredentials: true},
      ).then(function (response) {
            console.log(response.data)
            if ($.isEmptyObject(response.data.config)) {
                self.message = "There is no data"
            }
            else {
                self.config = response.data.config
                for (var id in self.config) {
                    let grid_item = self.config[id]
                    grid_item["i"] = id
                }
                // console.log(self.config)

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
