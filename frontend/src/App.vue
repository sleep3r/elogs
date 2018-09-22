<template>
    <div id="app">
        <base-page></base-page>
    </div>
</template>

<script>
    import BasePage from './components/BasePage.vue'

    export default {
        name: 'app',
        components: { BasePage }
    }
</script>

<style lang="scss">
    @import "./assets/scss/index.scss";
    #app {
        height: 100vh;
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
</style>
