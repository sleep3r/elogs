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
      axios.get('/furnace/fractional/granularity_gaphs/get')]).then(response => {
        if (!response[0].data.hasOwnProperty('data')) {
            console.info('Furnace data not found!');
            this.furnace_data = [];
        } else {
            this.furnace_data = response[0].data.data;
        }
        if (!response[1].data.hasOwnProperty('data')) {
            console.info('Graphs data not found!');
            this.gaphs_data = [];
        } else {
            this.gaphs_data = response[1].data.data;
        }
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
