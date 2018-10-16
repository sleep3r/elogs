<template>
    <main class="journal-page">
        <div class="journal-title">
            <h4 class="journal_title" v-if="$route.name === 'defaultJournalPage'">{{$store.getters['journalState/journalVerboseName']}}</h4>
            <button class="btn btn-outline" @click="openConstructor">
                Открыть в конструкторе
            </button>
        </div>
        <journal-panel></journal-panel>
        <article class="journal-tables">
            <template v-if="$store.getters['journalState/loaded']">
                <tablecommon v-for="(table, index) in $store.getters['journalState/tables']" :name="table" :index="index" :key="$store.getters['journalState/journalName']+'_'+table"></tablecommon>
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
    },
    methods: {
        openConstructor () {
            window.open('http://127.0.0.1:8085', '_blank')
        }
    },
    mounted () {
        console.log('mounted')
        this.$connect();
        window.parser.setVariable("CURRENT_SHIFT", this.$route.params.shift_id)
        console.log(this.$route.params)
        if (this.$route.params.shift_id) {
            this.$store.dispatch('journalState/loadJournal', {'id': this.$route.params.shift_id})
                .then((id) => {
                    this.$router.push('/' + this.$route.params.plant + '/' + this.$route.params.journal + '/' + id)
                    this.$store.dispatch('journalState/loadShifts', { plant: this.$route.params.plant, journal: this.$route.params.journal })
                })
        }
        else if (this.$route.params.plant && this.$route.params.journal) {
            this.$store.dispatch('journalState/loadJournal', {
              'plantName': this.$route.params.plant,
              'journalName': this.$route.params.journal
            })
                .then((id) => {
                    this.$router.push('/' + this.$route.params.plant + '/' + this.$route.params.journal + '/' + id)
                    this.$store.dispatch('journalState/loadShifts', { plant: this.$route.params.plant, journal: this.$route.params.journal })
                })
        }
    }
}
</script>

<style scoped>

</style>
