<template>
  <input class="general-value"
         type="text"
         v-bind:name="fieldName"
         v-bind:row-index="rowIndex"
         v-model="value" />
</template>

<script>
export default {
  name: 'Cell',
  props: {
      cellgroupInfo: Object,
      tableName: String,
      fieldName: String,
      rowIndex: Number
  },
  data() {
    return {
        value: ''
    }
  } ,
}
</script>
