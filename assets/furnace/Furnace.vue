<template>
  <div>
    <div 
      class="spinner-container" 
      v-if="loading">
      <spinner/>
    </div>
    <div v-else>
      <furnace-dashboard 
        :frac-data="furnace_array" 
        :gaphs-data="gaphs_data" />
    </div>

    <modals-container/>
  </div>
</template>

<script>
import axios from 'axios'
import Spinner from 'vue-simple-spinner'
import orderBy from 'lodash/orderBy'
import transform from 'lodash/transform'

import furnaceDashboard from './Dashboard.vue'
export default {
  name: 'Furnace',
  data() { 
    return {
      furnace_data: {},
      gaphs_data: {},
      loading: true
    }
  },
  computed: {
    furnace_array() {
      return orderBy(transform(this.furnace_data, (r, v, k) => {
        r.push(Object.assign({id: k}, v))
      }, []), frame => frame.cinder.time)
    }
  },
  created() {
    Promise.all([axios.get('/furnace/fractional/measurements/get'),
      axios.get('/furnace/fractional/granularity_gaphs/get')]).then(resp => {
        this.furnace_data = resp[0].data.data
        this.gaphs_data = resp[1].data.data
        this.loading = false
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
