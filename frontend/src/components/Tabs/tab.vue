<template>
    <section :class="[{'active': isActive}, 'tab-section']" v-show="isActive">
        <slot />
    </section>
</template>

<script>
    export default {
        name: "tab",
        props: {
          id: String
        },
        data() {
            return {
                isActive: false
            }
        }
    }
</script>

<style scoped>
    .tab-section{
        padding-top: 10px;
        text-align: left;
    }

</style>