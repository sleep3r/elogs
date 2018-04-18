<template>
  <div>
    <div v-if="furnace_array.length">
      <furnace-dashboard 
        :frac-data="furnace_array" 
        :gaphs-data="gaphs_data" />
    </div>
    <div 
      class="spinner-container" 
      v-else>
      <spinner/>
    </div>
    <modals-container/>
  </div>
</template>

<script>
import axios from 'axios'
import Spinner from 'vue-simple-spinner'

import furnaceDashboard from './Dashboard.vue'
export default {
  name: 'Furnace',
  data() { 
    return {
      furnace_data: {},
      gaphs_data: {}
    }
  },
  computed: {
    furnace_array() {
      return _.orderBy(_.transform(this.furnace_data, (r, v, k) => {
        r.push(v)
      }, []), frame => frame.cinder.time)
    }
  },
  created() {
    axios.get('/furnace/frac/measurements/get').then(({ data }) => {
      this.furnace_data = data.data
    })

    axios.get('/furnace/frac/granularity_gaphs/get').then(({ data }) => {
      this.gaphs_data = data.data
    })
  },
  components: {
    Spinner,
    furnaceDashboard
  }
}
</script>

<style>
.spinner-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center
}
</style>
