<template>
    <div class="field-description">
        <div class="model_value">
            <dl>
                <dt-item title="type" :value="model.value.type" />
                <dt-item title="min_normal" :value="model.value.min_normal" />
                <dt-item title="max_normal" :value="model.value.max_normal" />
                <dt-item title="units" :value="model.value.units" />
            </dl>
            <ul v-if="model.value.type === 'datalist'">
                <option v-for="opt in model.value.options">{{opt}}</option>
            </ul>
        </div>
        <div class="model_scope">
            <dl>
                <dt-item title="id" :value="model.scope.type" />
                <dt-item title="name" :value="model.scope.name" />
                <dt-item title="verbose_name" :value="model.scope.verbose_name" />
                <dt-item title="table" :value="model.scope.table" />
                <dt-item title="plant" :value="model.scope.plant" />
                <dt-item title="type" :value="model.scope.type" ></dt-item>
            </dl>
        </div>

    </div>
</template>

<script>
    import DtItem from './DtItem.vue';

    export default {
        name: "FieldDescription",
        props: {
            model: Object
        },
        components: {
            DtItem
        }
    }
</script>

<style scoped>

</style>