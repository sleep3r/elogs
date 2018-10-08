<template>
    <div class="field-description">
        <tabs :items="items" first=1>
            <tab id="1" >
                <div class="model_value">
                    <field-prop-edit section="value" name="type" :value="model.value.type" ></field-prop-edit>
                    <field-prop-edit section="value" name="min_normal" :value="model.value.min_normal" ></field-prop-edit>
                    <field-prop-edit title="max_normal" section="value" name="max_normal" :value="model.value.max_normal" ></field-prop-edit>
                    <field-prop-edit title="units" section="value" name="units" :value="model.value.units" ></field-prop-edit>
                    <ul class="list-group" v-if="model.value.type === 'datalist'">
                        <li v-for="opt in model.value.options" class="list-group-item" >{{opt}}</li>
                    </ul>
                </div>
            </tab>
            <tab id="2" >
                <div class="model_scope">
                    <field-prop-edit section="scope" name="id"  :value="model.scope.id" ></field-prop-edit>
                    <field-prop-edit  section="scope" name="name" :value="model.scope.name" ></field-prop-edit>
                    <field-prop-edit  section="scope" name="verbose_name" :value="model.scope.verbose_name" ></field-prop-edit>
                    <field-prop-edit  section="scope" name="table" :value="model.scope.table" ></field-prop-edit>
                    <field-prop-edit  section="scope" name="type" :value="model.scope.type" ></field-prop-edit>
                </div>
            </tab>
        </tabs>

    </div>
</template>

<script>
    import FieldPropEdit from "./FieldPropEdit.vue";
    import Tabs from "../../Tabs/tabs.vue";
    import Tab from "../../Tabs/tab.vue";

    // Vue.component('field-prop-edit', FieldPropEdit);

    export default {
        name: "SettingEdit",
        props: {
            model: Object
        },
        data() {
          return {
              items: [ {id: 1, title: 'Value'}, {id: 2, title: 'Scope'}]
          }
        },
        methods: {
            onInputChange(propName, value) {
                this.$store.commit('settingsState/UPDATE_MODEL_VALUE', {propName, value})
            }
        },
        components: {Tab, Tabs, FieldPropEdit}
    }
</script>

<style scoped>

</style>