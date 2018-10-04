<template>
    <div class="form-group">
        <label :for="fieldId">{{name}}</label>
        <input :id="fieldId" class="form-control" type="text" :value="value" @change="(event) => onChange(event.target.value)">
    </div>
</template>

<script>
    export default {
        name: "FieldPropEdit",
        props: [
            'section',
            'name',
            'value'
        ],
        computed: {
          fieldId: function(){
              return this.section + "_" + this.name
          }
        },
        methods: {
            onChange(value) {
                this.$store.commit('settingsState/UPDATE_MODEL_PROP', {
                    'sectionName': this.section,
                    'propName': this.name,
                    'value':value
                })
            }
        }
    }
</script>

<style scoped>

</style>