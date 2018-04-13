<template>
  <div> FURNACE
    <div class="x_panel">
      <div class="x_title">Cinder Date</div>
      <div class="x_content">
        <select name="center_data" class="form-control" v-model="cinder_index">
          <option v-for="(cinder, index) in cinder_data" :key="cinder.time" :value="index">{{ cinder.time }}</option>
        </select>
      </div>
      {{ cinder_current }}
    </div>
    <div class="x_panel">
      <div class="x_title">Schieht Date</div>
      <div class="x_content">
        <select name="center_data" class="form-control" v-model="schieht_index">
          <option v-for="(schieht, index) in cinder_data" :key="schieht.time" :value="index">{{ schieht.time }}</option>
        </select>
      </div>
      {{ schieht_current }}
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'app',
  data() { 
    return {
      furnace_data: {},
      cinder_index: -1,
      schieht_index: -1
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
    }
  },
  created() {
    axios.get('/furnace/frac/measurements/get').then(({ data }) => {
      this.furnace_data = data.data
    }) 
  }
}
</script>

