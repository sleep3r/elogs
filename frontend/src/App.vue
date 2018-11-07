<template>
    <div id="app">
        <router-view></router-view>
        <notifications classes='vue-notification'/>
    </div>
</template>

<script>
    export default {
        name: 'app',
        mounted () {
            if (this.$store.getters['userState/user']) {
                this.$connect()
                this.$store.dispatch('userState/getDefaultPage')
            }
        }
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
    .notifications {
        z-index: 4 !important;
    }
</style>
