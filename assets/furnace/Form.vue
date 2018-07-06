<template>
  <div class="fractional-form">
    <h2>Огарок</h2>
    <table>
      <tr>
        <td>Размер</td>
        <td
          v-for="(size, i) in cinder.min_sizes"
          :key="i">
          <input
            type="number"
            min="0"
            step="0.01"
            readonly
            v-model="cinder.min_sizes[i]">
        </td>
      </tr>
      <tr>
        <td>Масса</td>
        <td
          v-for="(mass, i) in cinder.masses"
          :key="i">
          <input
            type="number"
            min="0"
            step="0.01"
            v-model="cinder.masses[i]"></td>
      </tr>
    </table>
    <h2>Шихта</h2>
    <table>
      <tr>
        <td>Размер</td>
        <td
          v-for="(size, i) in schieht.min_sizes"
          :key="i">
          <input
            type="number"
            min="0"
            step="0.01"
            readonly
            v-model="schieht.min_sizes[i]">
        </td>
      </tr>
      <tr>
        <td>Масса</td>
        <td
          v-for="(mass, i) in schieht.masses"
          :key="i">
          <input
            type="number"
            min="0"
            step="0.01"
            v-model="schieht.masses[i]">
        </td>
      </tr>
    </table>
    <button @click="submit">OK</button>
    <button @click="$emit('close')">Не ОК</button>
  </div>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

export default {
  name: 'MeasurementForm',
  props: {
    timeframe: {
      type: Object,
      default: () => {}
    },
  },
  data() {
    return {
      cinder: {},
      schieht: {}
    }
  },
  created() {
    this.cinder = Object.assign({}, this.timeframe.cinder, this.timeframe.id ? {} 
    : {masses: new Array(this.timeframe.cinder.min_sizes.length).fill(0)})
    this.schieht = Object.assign({}, this.timeframe.schieht, this.timeframe.id ? {}
    : {masses: new Array(this.timeframe.schieht.min_sizes.length).fill(0)})
  },
  methods: {
    submit() {
      console.log('submit form')
      axios.post('/furnace/fractional/measurements/post', {
        cinder: this.cinder,
        schieht: this.schieht,
        id: this.timeframe.id
      }).then(({data}) => {
        this.$emit('close')
        if (!this.timeframe.id) {
          window.location.reload()
        }
      })
    }
  }
}
</script>

<style lang="scss">
  .fractional-form {
    input {
      width: 3em;
    }
  }
</style>
