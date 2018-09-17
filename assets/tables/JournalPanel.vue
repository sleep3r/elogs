<template>
    <div class="journal__panel">
        <div class="date-selector">
            <label>Выберите дату и смену</label>
            <input id="shift_field"
                   type="text"
                   :value="shiftFormatted"
                   v-on:click="showCalendar"
                   class="date-selector__date"
                   placeholder="Выберите дату..."

                   data-toggle="modal"
                   data-target="#myModal"
            >
        </div>
        <div class="mode-buttons">
            <!--{% if perms.all_journals_app.view_cells %}-->
                <button class="btn btn-view" v-on:click="changeMode('view')" >Просмотр</button>
            <!--{% endif %}-->
            <!--{% if 'all_journals_app.edit_cells' in perms and 'all_journals_app.modify_'|add:plant.name in perms %}-->
                <button class="btn btn-edit" v-on:click="changeMode('edit')">Редактирование</button>
            <!--{% endif %}-->
            <!--{% if 'all_journals_app.validate_cells' in perms and 'all_journals_app.modify_'|add:plant.name in perms %}-->
                <button class="btn btn-validate" v-on:click="changeMode('validate')">Валидация</button>
            <!--{% endif %}-->
            <!--{% for employee in employee_list %}-->
                <img style="height: 30px; width: 30px;" :title="employeeFormatted" src = "/static/images/no-avatar.png">
            <!--{% endfor %}-->
        </div>
        <modal v-show="isShowCalendar" @close="isShowCalendar = false" >
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
            isShowCalendar: false,
            shiftDate: '00-00-00',
            shiftOrder: '1',
            employeeName: 'Employee name',
            employeePosition: 'position',
            mode: '',
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
                    // $('#fc_create').click();
                    //
                    // let started = start;
                    // let ended = end;
                    //
                    // $(".antosubmit").on("click", function () {
                    //     var title = $("#title").val();
                    //     if (end) {
                    //         ended = end;
                    //     }
                    //
                    //     categoryClass = $("#event_type").val();
                    //
                    //     if (title) {
                    //         calendar.fullCalendar('renderEvent', {
                    //                 title: title,
                    //                 start: started,
                    //                 end: end,
                    //                 allDay: allDay
                    //             },
                    //             true // make the event "stick"
                    //         );
                    //     }
                    //
                    //     $('#title').val('');
                    //
                    //     calendar.fullCalendar('unselect');
                    //
                    //     $('.antoclose').click();

                        // return false;
                    // });
                },
                eventClick: function (calEvent, jsEvent, view) {
                    console.log("event click");
                    // $('#fc_edit').click();
                    // $('#title2').val(calEvent.title);
                    //
                    // categoryClass = $("#event_type").val();
                    //
                    // $(".antosubmit2").on("click", function () {
                    //     calEvent.title = $("#title2").val();
                    //
                    //     calendar.fullCalendar('updateEvent', calEvent);
                    //     $('.antoclose2').click();
                    // });
                    //
                    // calendar.fullCalendar('unselect');
                },
                editable: false,
            }
        }
    },
    computed: {
      shiftFormatted() {
          return  this.shiftDate + ", " + this.shiftOrder + "-ая смена";
      },
      employeeFormatted() {
          return this.employeeName + " : " + this.employeePosition;
      },
      getMode() {
          return this.getUrlParam('page_mode');
      }
    },
    methods: {
        changeMode(mode) {
            console.log("change mode to ", mode);
             let id = this.$root.pageId;
              function prepareUrl(mode) {
                  let url = location.pathname.concat(mode);
                      if (id !== null) {
                          url = url.concat("&id=" + id);
                      }
                  return url;
              }

              switch (mode) {
                  case 'view':
                      location.href = prepareUrl("?page_mode=view");
                     break;
                  case 'edit':
                     location.href = prepareUrl("?page_mode=edit");
                     break;
                  case 'validate':
                     location.href = prepareUrl("?page_mode=validate");
                     break;
                  default:
                     console.log("change mode to Default mode!");
                     break;
              }
        },
        showCalendar() {
            console.log("new showCalendar");
            this.isShowCalendar = true;
        },
        getUrlParam(paramName) {
           let url = window.location.search.substring(1);
           let urlParams = url.split('&');
           for (let i = 0; i < urlParams.length; i++) {
                let parameterName = urlParams[i].split('=');
                if (parameterName[0] === paramName) {
                    return parameterName[1];
                }
           }

           return "";
        }
    },
    mounted() {
       let selector = ".mode-buttons .btn-" + this.getMode;
       let activeBtn = document.querySelector(selector);
       if (activeBtn !== null) {
           activeBtn.classList.toggle("btn--active");
       }

        let plant = location.pathname.split('/')[1];
        let journal_name = location.pathname.split('/')[2];

        if (!plant || !journal_name) {
            plant = 'furnace';
            journal_name = 'fractional';
        }
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
