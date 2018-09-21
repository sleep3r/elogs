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
          <img style="height: 30px; width: 30px;"
               :title="employeeFormatted"
               src="/static/images/no-avatar.png">
        </div>
        <modal v-show="showCalendar" @close="showCalendar = false" >
            <full-calendar :events="events" :config="fullCalendarConfig" ref="calendar" />
        </modal>
    </div>
</template>
<script>
import axios from 'axios'
import 'jquery'
import { FullCalendar } from 'vue-full-calendar'
import modal from "./Modal.vue"

export default {
    name: 'journal-panel',
    data() {
        return {
            showCalendar: false,
            employeeName: 'Employee name',
            employeePosition: 'position',
            events: null,
            fullCalendarConfig: {
                locale: 'ru',
                buttonText: {
                  today:    'Сегодня',
                  month:    'Месяц',
                  week:     'Неделя',
                  day:      'День',
                  list:     'Список'
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
      employeeFormatted() {
          return this.employeeName + " : " + this.employeePosition;
      },
      mode() {
          return this.$store.state.journalInfo.mode;
      },
      shiftDate() {
        return this.$store.state.journalInfo.date;
      },
      shiftOrder() {
        return this.$store.state.journalInfo.order;
      }
    },
    methods: {
        changeMode(mode) {
          let permission = mode + '_cells'
          let permissions = this.$store.state.journalInfo.permissions
          for (let i=0; i<permissions.length; i++) {
            if (permission === permissions[i]) {
              this.$store.commit('SET_PAGE_MODE', mode);
            }
          }
        },
    },
    mounted() {
        let plant = location.pathname.split('/')[1];
        let journal_name = location.pathname.split('/')[2];

        let self = this;
        axios.get('/' + plant + '/' + journal_name +'/get_shifts/')
            .then(response => {
                self.events = response.data;
                $(".fc-month-button").click();
            })
            .catch(e => {
                console.log(e)
            });
    },
    components: {
        modal,
        FullCalendar
    }
}
</script>
<style>
</style>
