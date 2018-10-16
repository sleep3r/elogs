<template>
    <div class="journal__panel">
        <div class="date-selector">
            <label>Выберите дату и смену</label>
            <input id="shift_field"
                   type="text"
                   :value="shiftDate + ', ' + shiftOrder + '-ая смена'"
                   @click="showCalendar=true"
                   class="date-selector__date"
                   placeholder="Выберите дату..."
                   data-toggle="modal"
                   data-target="#myModal"
            >
        </div>
        <div class="panel-buttons">
            <div class="mode-buttons">
                <img v-for="employee of responsibles" style="height: 30px; width: 30px;"
                     :title="Object.values(employee)[0]"
                     src="../assets/images/no-avatar.png">
                <template v-if="userHasPerm('edit') && userHasPerm('validate')">
                <button :class="['btn', 'btn-edit', { 'btn--active': mode==='edit' }]"
                        @click="changeMode('edit')">
                    Редактирование
                </button>
                <button :class="['btn', 'btn-validate', { 'btn--active': mode==='validate' }]"
                        @click="changeMode('validate')">
                    Валидация
                </button>
              </template>
            </div>
            <button :class="['btn', 'btn-xlsx', 'float-right']"
                    @click="download_xlsx()">
                XLSX
            </button>
        </div>
        <div class="exp-time">
          <span v-if="((!shiftIsClosed)&&(shiftClosingTime))"> Смена открыта для редактирования {{ msToTime(remainingTime) }}</span>
          <span v-else>Смена закрыта для редактирования</span>
        </div>
        <modal v-show="showCalendar" @close="showCalendar = false">
            <full-calendar :events="events" :config="fullCalendarConfig" ref="calendar"/>
        </modal>
    </div>
</template>
<script>
    import $ from 'jquery'
    import EventBus from '../EventBus'
    import {FullCalendar} from 'vue-full-calendar'
    import modal from "./Modal.vue"
    let XLSX = require('xlsx');

    export default {
        name: 'journal-panel',
        data() {
            return {
                now: new Date(),
                showCalendar: false,
                employeeName: 'Employee name',
                employeePosition: 'position',
                fullCalendarConfig: {
                    locale: 'ru',
                    buttonText: {
                        today: 'Сегодня',
                        month: 'Месяц',
                        week: 'Неделя',
                        day: 'День',
                        list: 'Список'
                    },
                    timeFormat: 'H(:mm)',
                    header: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'month, listMonth'
                    },
                    selectable: true,
                    selectHelper: true,
                    select: function (start, end, allDay) {
                    },
                    eventClick: function (calEvent, jsEvent, view) {
                        console.log("event click");
                    },
                    editable: false,
                }
            }
        },
        computed: {
            remainingTime() {
                if (!(this.shiftClosingTime)) {
                    return -1;
                }
                console.log('shift closing time ' + this.shiftClosingTime)
                console.log('now ' + this.now)
                let remainingTime = this.shiftClosingTime - this.now
                if (remainingTime < 0) {
                  for (let perm of ['validate', 'view']) {
                      if (this.userHasPerm(perm)) {
                          this.$store.commit('journalState/SET_PAGE_MODE', perm)
                          break
                      }
                  }
                }
                return ((remainingTime) && (remainingTime > 0)) ? remainingTime : 0
            },
            shiftIsClosed() {
                if (this.remainingTime == 0) {
                    return true
                }
                else {
                    return this.$store.getters['journalState/journalInfo'].closed
                }
            },
            shiftClosingTime() {
                let time = this.$store.getters['journalState/journalInfo'].permissions.time
                return time ? Date.parse(time['shift_closing']) : null
            },
            editingModeClosingTime() {
                let time = this.$store.getters['journalState/journalInfo'].permissions.time
                return time ? Date.parse(['editing_mode_closing']) : null
            },
            responsibles() {
                return this.$store.getters['journalState/journalInfo'].responsibles
            },
            events() {
                return this.$store.getters['journalState/events'];
            },
            employeeFormatted() {
                return this.employeeName + " : " + this.employeePosition;
            },
            mode() {
                return this.$store.getters['journalState/journalInfo'].mode;
            },
            shiftDate() {
                return this.$store.getters['journalState/journalInfo'].date;
            },
            shiftOrder() {
                return this.$store.getters['journalState/journalInfo'].order;
            },
        },
        methods: {
            userHasPerm(perm) {
                for (let p of this.$store.getters['journalState/journalInfo'].permissions.permissions) {
                    if (p == perm) {
                        return true
                    }
                }
              return false
            },
            changeMode(mode) {
                if (mode === 'edit') {
                    $('.resp-modal').addClass('resp-modal__open')
                    EventBus.$emit('open-resp-modal')
                }

                this.$store.commit('journalState/SET_PAGE_MODE', mode);
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
        mounted() {
            let self = this;
            this.$store.dispatch('journalState/loadShifts', {
                plant: this.$route.params.plant,
                journal: this.$route.params.journal
            })

            $( window ).resize(function() {
                console.log('resize')
                setTimeout(() => {
                    $('.fc-scroller.fc-day-grid-container').css({'overflow': 'auto', 'height': '400px'})
                }, 100)
            })

            $('.fc-toolbar.fc-header-toolbar button').click(function () {
                setTimeout(() => {
                    $('.fc-scroller.fc-day-grid-container').css({'overflow': 'auto', 'height': '400px'})
                }, 1)
            })
        },
        components: {
            modal,
            FullCalendar
        },
        created() {
            setInterval(() => this.now = (new Date()).getTime(), 1000)
        }
    }
</script>
<style>

</style>
