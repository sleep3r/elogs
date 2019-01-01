<template>
    <main class="journal-page">
        <template v-if="$store.getters['journalState/loaded']">
            <div class="journal_title_container">
                <div class="exp-time" :style="{'background-color': canEdit ? '#02a202' : '#d80000'}"><span> {{ shiftMessage }} </span></div>
                <div style="width: 100%; padding: 6px 15px;">
                    <div class="journal-title">
                        <h5 class="journal_title" v-if="$route.name === 'defaultJournalPage'">{{$store.getters['journalState/journalVerboseName']}}</h5>
                        <div class="actions-icons">
                            <i class="fas fa-file-excel" @click="download_xlsx()" data-toggle="tooltip" title="Скачать xlsx"></i>
                            <i
                                class="fas fa-edit"
                                v-if="$store.getters['userState/isBoss'] || $store.getters['userState/isSuperuser']"
                                @click="openConstructor"
                                data-toggle="tooltip"
                                style="margin-left: 18px;"
                                title="Открыть в конструкторе"
                            ></i>
                        </div>
                    </div>
                    <journal-panel></journal-panel>
                </div>
            </div>
            <div class="journal_title_container__background">
                <h4 class="journal_title" v-if="$route.name === 'defaultJournalPage'">{{$store.getters['journalState/journalVerboseName']}}</h4>
                <journal-panel></journal-panel>
            </div>
            <div class="journal-tables" :style="{paddingTop: paddingTop}">
                <template v-if="$store.getters['journalState/loaded']">
                    <tablecommon v-for="(table, index) in $store.getters['journalState/tables']" :name="table" :index="index" :key="$store.getters['journalState/journalName']+'_'+table"></tablecommon>
                </template>
                <template v-else >
                    <span>Нет данных</span>
                </template>
            </div>
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
    let XLSX = require('xlsx');


    export default {
        name: "JournalPage",
        data () {
            return {
                shiftMessage: '',
                now: new Date(),
                paddingTop: '110px'
            }
        },
        watch: {
            now (value) {
                this.updateShiftMode();
            },
        },
        computed: {
            canEdit () {
                return (((!this.timeLimits) && this.userHasPerm('edit')) || this.$store.getters['userState/isSuperuser']) ||
                    (this.remainingTime && this.userHasPerm('edit'))
            },
            remainingTime() {
                // time before shift editing will be closed
                let deadline = 0
                if ((this.userIsResponsible)&&(this.timeLimits['editing_mode_closing'])) {
                    deadline = this.shiftClosingTime
                }
                else {
                    deadline = this.editingModeClosingTime
                }
                let remainingTime = deadline - this.now

                return ((remainingTime) && (remainingTime > 0)) ? remainingTime : 0
            },
            shiftIsClosed() {
                return this.$store.getters['journalState/journalInfo'].closed
            },
            shiftStartTime() {
                return Date.parse(this.$store.getters['journalState/journalInfo']['start_time'])
            },
            shiftIsStarted() {
                return (this.now - this.shiftStartTime) > 0 ? true : false
            },
            shiftClosingTime() {
                return Date.parse(this.timeLimits['shift_closing'])
            },
            timeLimits() {
                return this.$store.getters['journalState/journalInfo'].permissions.time
            },
            editingModeClosingTime() {
                if (this.timeLimits) {
                    return Date.parse(this.timeLimits['editing_mode_closing'])
                }
                else {
                    return null
                }
            },
        },
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
                    : window.FRONT_CONSTRUCTOR_HOSTNAME}/journal/${this.$route.params.journal}?plant=${this.$route.params.plant}&imported=true&version=${this.$store.getters['journalState/journalVersion']}`,
                '_blank')
            },
            download_xlsx() {
                let elt = $('.elog-journal-table').clone();
                elt.find("td").replaceWith(function () {
                    return '<td>' + $(this).find("input.general-value").val() + '</td>';
                });
                let tables = elt.get();

                const new_workbook = XLSX.utils.book_new();
                for (let i = 0; i < tables.length; i++) {
                    let ws = XLSX.utils.table_to_sheet(tables[i]);
                    XLSX.utils.book_append_sheet(new_workbook, ws, "table" + i);
                }

                XLSX.writeFile(new_workbook, 'journal.xlsx');
            },
            removePerm(perm) {
                if (this.userHasPerm(perm)) {
                    this.$store.commit('journalState/REMOVE_PERMISSION', perm)
                }
            },
            updateShiftMode() {
                if (((!this.timeLimits) && this.userHasPerm('edit')) || this.$store.getters['userState/isSuperuser']) {
                    this.shiftMessage = 'Журнал открыт для редактирования'
                }
                else if ((!this.userHasPerm('edit'))) {
                    this.shiftMessage = 'Вы не можете редактировать данный журнал'
                    this.removePerm('edit')
                }
                else if (!this.shiftIsStarted) {
                    this.shiftMessage = 'Смена ещё не началась. Редактирование невозможно'
                    this.removePerm('edit')
                }
                else if (this.shiftIsClosed) {
                    this.shiftMessage = 'Смена закрыта для редактирования. Обратитесь к администратору'
                    this.removePerm('edit')
                }
                else if ((!this.userIsResponsible) && (this.now > this.editingModeClosingTime)) {
                    this.shiftMessage = 'Смена закрыта для редактирования (до конца смены меньше часа, а редактирование начато не было)'
                    this.removePerm('edit')
                }
                else if ((this.userIsResponsible) && (this.now > this.shiftClosingTime)) {
                    this.shiftMessage = 'Смена закрыта для редактирования (прошло 12 часов с конца смены)'
                    this.removePerm('edit')
                }
                else if (this.remainingTime && this.userHasPerm('edit')) {
                    this.shiftMessage = 'Смена открыта для редактирования ещё ' + this.msToTime(this.remainingTime)
                }
            },
            msToTime(s) {
                var ms = s % 1000;
                s = (s - ms) / 1000;
                var secs = s % 60;
                s = (s - secs) / 60;
                var mins = s % 60;
                var hrs = (s - mins) / 60;

                return hrs + ' часов ' + mins + ' минут ' + secs + ' секунд';
            }
        },
        updated () {
            setTimeout(() => this.paddingTop = ($('.journal_title_container').height() + ($(window).width() < 678 ? 104 : 10)) + 'px', 0)
        },
        mounted() {
            $('[data-toggle="tooltip"]').tooltip({delay: {show: 200, hide: 0}})

            this.updateShiftMode()
            // console.log('mounted')
            let shift_id = this.$route.params.shift_id;
            window.parser.setVariable("CURRENT_SHIFT", "0")
            if (this.$route.params.shift_id) {
                this.$store.dispatch('formulaState/loadLastShifts', {
                    'plantName': this.$route.params.plant,
                    'journalName': this.$route.params.journal
                })
                this.$store.dispatch('journalState/loadJournal', {'id': this.$route.params.shift_id})
                    .then((id) => {
                        this.$router.push('/' + this.$route.params.plant + '/' + this.$route.params.journal + '/' + id)
                    })
            }
            else if (this.$route.params.plant && this.$route.params.journal) {
                this.$store.dispatch('formulaState/loadLastShifts', {
                    'plantName': this.$route.params.plant,
                    'journalName': this.$route.params.journal
                })
                this.$store.dispatch('journalState/loadJournal', {
                    'plantName': this.$route.params.plant,
                    'journalName': this.$route.params.journal
                })
                    .then((id) => {
                        this.$router.push('/' + this.$route.params.plant + '/' + this.$route.params.journal + '/' + id)
                    })
            }
        },
        created() {
            setInterval(() => this.now = (new Date()).getTime(), 1000)
        }
    }
</script>

<style scoped>

.journal_title {
    margin-bottom: 0;
}

</style>
