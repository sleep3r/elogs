<template>
    <div class="elogs-container">
        <top-nav></top-nav>
        <div class="main-container">
            <nav class="column-left">
                <left-menu v-if="$route.name !== 'modesPage'"></left-menu>
                <modes-left-menu v-else></modes-left-menu>
            </nav>
            <div class="column-content" id="elogs-app">
                <router-view></router-view>
                <main-footer></main-footer>
            </div>
        </div>
        <popup></popup>
    </div>
</template>

<script>
    import TopNav from './TopNav.vue'
    import Menu from './Menu.vue'
    import ModesMenu from './ModesMenu.vue'
    import Footer from './Footer.vue'
    import Popup from './Popup.vue';

    export default {
        name: "BasePage",
        components: {
            'top-nav': TopNav,
            'left-menu': Menu,
            'modes-left-menu': ModesMenu,
            'main-footer': Footer,
            'popup': Popup,
        },
        methods: {},
        mounted() {

        }
    }
</script>

<style scoped>

</style>
