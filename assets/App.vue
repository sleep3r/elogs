<template>
  <div>
    <div v-if="furnace_array.length">
      <furnace :frac-data="furnace_array" />
    </div>
    <div class="spinner-container" v-else>
      <spinner/>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Spinner from 'vue-simple-spinner'

import furnace from './Furnace.vue'
export default {
  name: 'app',
  data() { 
    return {
      furnace_data: {}
    }
  },
  computed: {
    furnace_array() {
      return _.transform(this.furnace_data, (r, v, k) => {
        r.push(v)
      }, [])
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
    furnace
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
