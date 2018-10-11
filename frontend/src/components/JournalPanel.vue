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
                <img style="height: 30px; width: 30px;"
                     :title="employeeFormatted"
                     src="../assets/images/no-avatar.png">
                <button v-if="viewIsAllowed" :class="['btn', 'btn-view', { 'btn--active': mode==='view' }]"
                        @click="changeMode('view')">
                    Просмотр
                </button>
                <button v-if="editIsAllowed" :class="['btn', 'btn-edit', { 'btn--active': mode==='edit' }]"
                        @click="changeMode('edit')">
                    Редактирование
                </button>
                <button v-if="validateIsAllowed" :class="['btn', 'btn-validate', { 'btn--active': mode==='validate' }]"
                        @click="changeMode('validate')">
                    Валидация
                </button>
            </div>
            <button :class="['btn', 'btn-xlsx', 'float-right']"
                    @click="download_xlsx()">
                XLSX
            </button>
        </div>
        <modal v-show="showCalendar" @close="showCalendar = false">
            <full-calendar :events="events" :config="fullCalendarConfig" ref="calendar"/>
        </modal>
    </div>
</template>
<script>
    import $ from 'jquery'
    import {FullCalendar} from 'vue-full-calendar'
    import modal from "./Modal.vue"
    let XLSX = require('xlsx');

    export default {
        name: 'journal-panel',
        data() {
            return {
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
            viewIsAllowed() {
              for (let perm of this.$store.getters['journalState/journalInfo'].permissions.permissions) {
                  if (perm == 'view') {
                      return true
                  }
              }
              return false
            },
            editIsAllowed() {
                // period of time when shift can be edited
                let editTime = this.$store.getters['journalState/journalInfo'].permissions.time
                var d = new Date();
                var n = d.toISOString();
                console.log(Date.parse(editTime[0]) + ' < ' + Date.parse(n) + ' < ' + Date.parse(editTime[1]))
                return ((Date.parse(editTime[0]) <= Date.now()) && (Date.now() <= Date.parse(editTime[1])))
            },
            validateIsAllowed() {
                for (let perm of this.$store.getters['journalState/journalInfo'].permissions.permissions) {
                    if (perm == 'validate') {
                        return true
                    }
                }
                return false
            }
        },
        methods: {
            changeMode(mode) {
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
        },
        mounted() {
            let self = this;
            this.$store.dispatch('journalState/loadShifts', {
                plant: this.$route.params.plant,
                journal: this.$route.params.journal
            })
        },
        components: {
            modal,
            FullCalendar
        }
    }
</script>
<style>

</style>
