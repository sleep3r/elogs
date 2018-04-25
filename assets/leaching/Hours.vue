<template>
   <select class="form-control" v-model="hour" slot="one" @change="onChange" >
       <option disabled value="">Please select one</option>
       <option value="8" >8:00</option>
       <option value="10" >10:00</option>
       <option value="12" >12:00</option>
       <option value="14" >14:00</option>
       <option value="16" >16:00</option>
       <option value="18" >18:00</option>
       <option value="20" >20:00</option>
   </select>
</template>
<script>
export default {
  name: 'SelectHours',
  props: {
     current: {
        type: Number,
        default: 8
     }
  },
  data() {
    return {
      hour: 0,
      options: []
    }
  },
  computed: {

  },
  methods: {
        onChange(event) {
            let selectedHour = event.target.value
            console.log(selectedHour)
            this.$emit('selectedHour', selectedHour)
        }
  }
}
</script>