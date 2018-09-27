<template>
    <div class="elogs-container">
        <top-nav></top-nav>
        <div class="main-container">
            <nav class="column-left">
                <left-menu></left-menu>
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
import Footer from './Footer.vue'
import Popup from './Popup.vue';

export default {
    name: "BasePage",
    components: {
        'top-nav': TopNav,
        'left-menu': Menu,
        'main-footer': Footer,
        'popup': Popup,
    },
    mounted () {
        if (this.$route.params.shift_id) {
            this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id)
        }
    }
}
</script>

<style scoped>

</style>