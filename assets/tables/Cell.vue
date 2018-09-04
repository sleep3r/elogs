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
  props: [
      'cellgroupInfo',
      'tableName',
      'fieldName',
      'rowIndex',
  ],
  data() {
    return {
        value: ''
    }
  } ,
}
</script>
