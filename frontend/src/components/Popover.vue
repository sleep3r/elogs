<template>
    <div class="popover" v-bind:style="{display: show ? 'block' : 'none', left: x + 'px', top: y + 'px'}">
        <slot>

        </slot>
    </div>
</template>

<script>
import ajax from '../axios.config'
import EventBus from '../EventBus'

export default {
  name: 'Popover',
  props: [
    'show',
    'x',
    'y'
  ],
  data: function() {
      return {
          
      }
  },
  computed: {
    
  },
  methods: {
    
  },
  mounted () {
      
  }
}
</script>

<style lang="scss">

</style>
