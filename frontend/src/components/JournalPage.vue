<template>
    <main class="journal-page" data-mode="?? page_mode ??">
        <journal-panel></journal-panel>
        <article class="journal-tables">
            <template v-if="$store.getters['journalState/loaded']">
                <tablecommon v-for="table in $store.getters['journalState/tables']" :name="table"></tablecommon>
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
    methods: {
        setConnectionListeners () {
            let _this = this
            $(window).on('online', function () {
                _this.synchronizeCells()
            })
        },
        synchronizeCells () {
            let unsyncCells = this.$store.getters['journalState/unsyncJournalCells']()
            // let unsyncCellPromises = unsyncCells.map(item => new Promise((res, rej) => {
            //     this.$socket.sendObj({
            //         'type': 'shift_data',
            //         'cell_location': {
            //             'group_id': this.$store.getters['journalState/journalInfo'].id,
            //             'table_name': item.tableName,
            //             'field_name': item.fieldName,
            //             'index': item.index
            //         },
            //         'value': item.value
            //     });
            //     console.log(1111111111111111111)
            //     res()
            // }))
            //
            // Promise.all(unsyncCellPromises)
            //     .then(() => {
            //         this.$store.commit('journalState/SET_SYNCHRONIZED', true)
            //         if (this.$route.params.shift_id) {
            //             this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id)
            //         }
            //     })


            unsyncCells.map(item => {
                this.$socket.sendObj({
                    'type': 'shift_data',
                    'cell_location': {
                        'group_id': this.$store.getters['journalState/journalInfo'].id,
                        'table_name': item.tableName,
                        'field_name': item.fieldName,
                        'index': item.index
                    },
                    'value': item.value
                });
                console.log(1111111111111111111)
            })

            this.$store.commit('journalState/SET_SYNCHRONIZED', true)
            if (this.$route.params.shift_id) {
                this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id)
            }
        }
    },
    updated () {
        this.setConnectionListeners()

        if (navigator.onLine && !this.$store.getters['journalState/isSynchronized']) {
            this.synchronizeCells()
        }
    },
    mounted () {
        this.$connect();

        if (navigator.onLine && this.$store.getters['journalState/isSynchronized'] && this.$route.params.shift_id) {
            this.$store.dispatch('journalState/loadJournal', this.$route.params.shift_id)
        }
        else if (navigator.onLine && !this.$store.getters['journalState/isSynchronized']) {
            this.synchronizeCells()
        }
    }
}
</script>

<style scoped>

</style>
