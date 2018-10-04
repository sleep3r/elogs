<template>
    <span v-if="value">
        <dt>{{title}}</dt>
        <dd>{{value}}</dd>
    </span>

</template>

<script>
    export default {
        name: "DtItem",
        props: {
            title: String,
            value: String
        }
    }
</script>

<style scoped>

</style>