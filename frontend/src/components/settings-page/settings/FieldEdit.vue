<template>
    <div class="field-description">
        <div class="model_value">
            <field-prop-edit title="type" :value="model.value.type" ></field-prop-edit>
            <field-prop-edit title="min_normal" :value="model.value.min_normal" ></field-prop-edit>
            <field-prop-edit title="max_normal" :value="model.value.max_normal" ></field-prop-edit>
            <field-prop-edit title="units" :value="model.value.units" ></field-prop-edit>
            <ul class="list-group" v-if="model.value.type === 'datalist'">
                <li v-for="opt in model.value.options" class="list-group-item" >{{opt}}</li>
            </ul>
        </div>
        <div class="model_scope">
            <field-prop-edit title="id" :value="model.scope.id" ></field-prop-edit>
            <field-prop-edit title="name" :value="model.scope.name" ></field-prop-edit>
            <field-prop-edit title="verbose_name" :value="model.scope.verbose_name" ></field-prop-edit>
            <field-prop-edit title="table" :value="model.scope.verbose_name" ></field-prop-edit>
            <field-prop-edit title="type" :value="model.scope.type" ></field-prop-edit>
        </div>
    </div>
</template>

<script>
    import FieldPropEdit from "./FieldPropEdit";
    export default {
        name: "FieldEdit",
        components: {FieldPropEdit},
        props: {
            model: Object
        }
    }
</script>

<style scoped>

</style>