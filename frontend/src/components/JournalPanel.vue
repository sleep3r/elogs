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
        <div class="mode-buttons">
            <img style="height: 30px; width: 30px;"
                 :title="employeeFormatted"
                 src="../assets/images/no-avatar.png">
            <button :class="['btn', 'btn-view', { 'btn--active': mode==='view' }]"
                    @click="changeMode('view')">
                Просмотр
            </button>
            <button :class="['btn', 'btn-edit', { 'btn--active': mode==='edit' }]"
                    @click="changeMode('edit')">
                Редактирование
            </button>
            <button :class="['btn', 'btn-validate', { 'btn--active': mode==='validate' }]"
                    @click="changeMode('validate')">
                Валидация
            </button>
        </div>
        <button :class="['btn', 'btn-xlsx', 'float-right']"
                @click="download_xlsx()">
            XLSX
        </button>
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
            }
        },
        methods: {
            changeMode(mode) {
                let permission = mode + '_cells';
                let permissions = this.$store.getters['journalState/journalInfo'].permissions.permissions;
                for (let i = 0; i < permissions.length; i++) {
                    if (permission === permissions[i]) {
                        this.$store.commit('journalState/SET_PAGE_MODE', mode);
                    }
                }
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
    .btn-xlsx {
        margin-left: auto;
        margin-right: 20px;
    }
</style>
