<template>
  <div> FURNACE
    <span v-if="furnace_data['1']"> {{ furnace_data }} </span>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data() { 
    return {
      furnace_data: {}
    }
  },
  created() {
    axios.get('/furnace/frac/measurements/get').then(({ data }) => {
      this.furnace_data = data.data
    }) 
  }
}
</script>

