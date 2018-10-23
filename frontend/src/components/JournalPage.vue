<template>
    <main class="journal-page">
        <template v-if="$store.getters['journalState/loaded']">
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
        </template>
        <template v-else >
            <div class="spinner-container"><i class="spinner"></i></div>
        </template>
    </main>
</template>

<script>
import TableCommon from './TableCommon.vue';
import JournalPanel from './JournalPanel.vue';
import ajax from "../axios.config"


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
            window.open(`http://${window.location.hostname === 'localhost' ?
                '127.0.0.1'
                : window.location.hostname}:8085/journal/${this.$route.params.journal}?plant=${this.$route.params.plant}&imported=true`,
            '_blank')
        }
    },
    mounted() {
        // console.log('mounted')
        this.$connect();
        let shift_id = this.$route.params.shift_id;
        window.parser.setVariable("CURRENT_SHIFT", shift_id)
        ajax.get(`http://localhost:8000/api/prev-shift/?shift_id=${shift_id}`,
            {
                withCredentials: true
            }).then(
            (res) => {
                window.parser.setVariable("PREV_SHIFT", res.data)
            })
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
