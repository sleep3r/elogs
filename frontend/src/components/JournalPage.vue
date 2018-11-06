<template>
    <main class="journal-page">
        <template v-if="$store.getters['journalState/loaded']">
            <div class="journal_title_container">
                <h4 class="journal_title" v-if="$route.name === 'defaultJournalPage'">{{$store.getters['journalState/journalVerboseName']}}</h4>
                <button v-if="$store.getters['userState/isBoss'] || $store.getters['userState/isSuperuser']" class="btn btn-outline" @click="openConstructor">
                    Открыть в конструкторе
                </button>
                <journal-panel></journal-panel>
            </div>
            <div class="journal_title_container__background">
                <h4 class="journal_title" v-if="$route.name === 'defaultJournalPage'">{{$store.getters['journalState/journalVerboseName']}}</h4>
                <journal-panel></journal-panel>
            </div>
            <article class="journal-tables">
                <template v-if="$store.getters['journalState/loaded']">
                    <tablecommon v-for="(table, index) in $store.getters['journalState/tables']" :name="table" :index="index" :key="$store.getters['journalState/journalName']+'_'+table"></tablecommon>
                </template>
                <template v-else >
                    <span>Нет данных</span>
                </template>
            </article>
        </template>
        <template v-else >
            <div class="spinner-container"><i class="spinner"></i></div>
        </template>
    </main>
</template>

<script>
import TableCommon from './TableCommon.vue';
import JournalPanel from './JournalPanel.vue';
var request = require('sync-request');


export default {
    name: "JournalPage",
    components: {
        'tablecommon': TableCommon,
        'journal-panel': JournalPanel
    },
    updated() {
        for (let perm of ['validate', 'edit', 'view']) {
            // console.log(perm)
            if (this.userHasPerm(perm)) {
                this.$store.commit('journalState/SET_PAGE_MODE', perm)
                break
            }
        }
    },
    methods: {
      userHasPerm(perm) {
          if (perm == 'view') {
              return true
          }
          for (let p of this.$store.getters['journalState/journalInfo'].permissions.permissions) {
              if (p == perm) {
                  return true
              }
          }
          return false
        },
        openConstructor() {
            window.open(`${window.location.hostname === 'localhost' ?
                'http://127.0.0.1:8085'
                : window.FRONT_CONSTRUCTOR_HOSTNAME}/journal/${this.$route.params.journal}?plant=${this.$route.params.plant}&imported=true`,
            '_blank')
        }
    },
    mounted() {
        // console.log('mounted')
        let shift_id = this.$route.params.shift_id;
        window.parser.setVariable("CURRENT_SHIFT", shift_id)
        var res = request("GET", window.HOSTNAME + `/api/prev-shift/?shift_id=${shift_id}`)
        let json = JSON.parse(res.getBody())
        window.parser.setVariable("PREV_SHIFT", json)
        // ajax.get(`http://localhost:8000/api/prev-shift/?shift_id=${shift_id}`).then(
        //     (res) => {
        //         window.parser.setVariable("PREV_SHIFT", res.data)
        //     })
        // console.log(this.$route.params)
        if (this.$route.params.shift_id) {
            this.$store.dispatch('journalState/loadJournal', {'id': this.$route.params.shift_id})
                .then((id) => {
                    this.$router.push('/' + this.$route.params.plant + '/' + this.$route.params.journal + '/' + id)
                })
        }
        else if (this.$route.params.plant && this.$route.params.journal) {
            this.$store.dispatch('journalState/loadJournal', {
              'plantName': this.$route.params.plant,
              'journalName': this.$route.params.journal
            })
                .then((id) => {
                    this.$router.push('/' + this.$route.params.plant + '/' + this.$route.params.journal + '/' + id)
                })
        }
    }
}
</script>

<style scoped>

</style>
