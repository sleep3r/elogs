<template>
    <div class="elogs-container">
        <top-nav></top-nav>
        <div class="main-container">
            <nav class="column-left">
                <left-menu></left-menu>
            </nav>
            <div class="column-content" id="elogs-app">
                <main class="journal-page" data-mode="?? page_mode ??">
                    <journal-panel></journal-panel>
                    <article class="journal-tables">
                        <template v-if="$store.getters['journalState/loaded']">
                            <tablecommon name="?? table_name ??" ></tablecommon>
                        </template>
                        <template v-else >
                            <span>Нет данных</span>
                        </template>
                    </article>
                </main>
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
import TableCommon from './TableCommon.vue';
import JournalPanel from './JournalPanel.vue';
import Popup from './Popup.vue';

export default {
    name: "BasePage",
    components: {
        'top-nav': TopNav,
        'left-menu': Menu,
        'main-footer': Footer,
        'tablecommon': TableCommon,
        'journal-panel': JournalPanel,
        'popup': Popup,
    },
    mounted () {
        this.$store.dispatch('journalState/loadJournal', 18);
    }
}
</script>

<style scoped>

</style>