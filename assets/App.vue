<template>
  <div>
    <div v-if="cinder_data.length">
    <div class="x_panel">
      <div class="x_title">Cinder Date</div>
      <div class="x_content">
        <select name="center_data" class="form-control" v-model="cinder_index">
          <option v-for="(cinder, index) in cinder_data" :key="cinder.time" :value="index">{{ cinder.time }}</option>
        </select>
      </div>
      CINDER
      <div class="carousel">
        <div class="timeframe" v-for="timeframe in current_timeframes" :key="timeframe.cinder.time">
          <span>{{ timeframe.cinder.time }}</span>
        <bar-chart
        :min-sizes="timeframe.cinder.min_sizes"
        :masses="timeframe.cinder.masses"></bar-chart>
        <bar-chart :min-sizes="timeframe.schieht.min_sizes" :masses="timeframe.schieht.masses"></bar-chart>
        <span>{{ timeframe.schieht.time }}</span>
        </div>
      </div>
        
            SCHIEHT
    </div>
  </div>
  <div class="spinner-container" v-else>
    <spinner/>
  </div>
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'

import Spinner from 'vue-simple-spinner'
import barChart from './BarChart.vue'

export default {
  name: 'app',
  data() { 
    return {
      furnace_data: {},
      cinder_index: 0,
      // schieht_index: 0
    }
  },
  computed: {
    cinder_data() {
      return _.transform(this.furnace_data, (r, v, k) => {
        r.push(v.cinder)
      }, [])
    },
    cinder_current() {
      return this.cinder_data[this.cinder_index]
    },
    schieht_data() {
      return _.transform(this.furnace_data, (r, v, k) => {
        r.push(v.schieht)
      }, [])
    },
    schieht_current() {
      return this.schieht_data[this.schieht_index]
    },
    schieht_index() {
      return this.cinder_index
    },
    furnace_array() {
      return _.transform(this.furnace_data, (r, v, k) => {
        r.push(v)
      }, [])
    },
    current_timeframes() {
      let frame = 3
      let index = this.cinder_index
      return this.furnace_array.slice(Math.max(0, index - 1), Math.min(this.furnace_array.length - 1, index ? index + 2 : 3))
    }
  },
  created() {
    // furnace/frac/measurements/get
    axios.get('/static/frac/f.json').then(({ data }) => {
      this.furnace_data = data.data
    }) 
  },
  components: {
    Spinner,
    barChart
  }
}
</script>

<style>
  .carousel {
    display: flex;
  }

  .carousel .timeframe {
    display: flex;
    flex-direction: column;
    height: 600px;
    align-items: center;
  }

.spinner-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center
}
</style>

