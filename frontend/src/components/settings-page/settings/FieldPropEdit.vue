<template>
    <div class="form-group">
        <label>{{title}}</label>
        <input class="form-control" type="text" v-model="value">
    </div>
</template>

<script>
    export default {
        name: "FieldPropEdit",
        props: [
            'title',
            'value'
        ]
    }
</script>

<style scoped>

</style>