<template>
    <main class="journal-page" data-mode="?? page_mode ??">
        <journal-panel></journal-panel>
        <article class="journal-tables">
            <template v-if="$store.getters['journalState/loaded']">
                <tablecommon v-for="table in $store.getters['journalState/tables']" :name="table" :key="$store.getters['journalState/journalName']+'_'+table"></tablecommon>
            </template>
            <template v-else >
                <span>Нет данных</span>
            </template>
        </article>
    </main>
</template>

<script>
import TableCommon from './TableCommon.vue';
import JournalPanel from './JournalPanel.vue';

export default {
    name: "JournalPage",
    components: {
        'tablecommon': TableCommon,
        'journal-panel': JournalPanel
    },
    updated () {
        // if (this.$route.params.shift_id) {
        //     this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id)
        // }
    },
    mounted () {
        console.log('mounted')
        this.$connect();

        if (this.$route.params.shift_id) {
            this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id)
        }
    }
}
</script>

<style scoped>

</style>
