<template>
  <input class="general-value"
         type="text"
         v-bind:name="fieldName"
         v-bind:row-index="rowIndex"
         v-model="value"
         v-on:input="onInput"
         v-on:change="onChanged"
  />
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
  },
  methods: {
      onInput() {
          
      },
      onChanged() {
          console.info("table-name: ", this.tableName, "field-name: ", this.fieldName, "value: ", this.value);
      }
  }
}
</script>
