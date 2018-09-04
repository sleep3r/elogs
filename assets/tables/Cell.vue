<template>
  <input :class="classes"
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
      'fieldName',
      'rowIndex',
  ],
  data() {
    return {
        value: '',
        classes: 'general-value number-cell form-control'
    }
  },
  computed: {
    tableName: function() {
        return this.$parent.props.tableName;
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
