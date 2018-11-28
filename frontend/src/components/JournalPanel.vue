<template>
    <div class="journal__panel">
        <div class="shift-container">

            <div v-if="journalType === 'shift'" class="date-selector" data-toggle="tooltip" title="Выберите дату и смену">
                <input id="shift_field"
                    type="text"
                    :value="shiftDate + ', ' + shiftOrder + '-ая смена'"
                    @click="showCalendar=true"
                    class="date-selector__date"
                    placeholder="Выберите дату..."
                    data-toggle="modal"
                    data-target="#FullCalendarModal"
                >
            </div>
            <div v-else-if="journalType === 'year'" class="date-selector" data-toggle="tooltip" title="Выберите год">
                <input id="year_field"
                    type="text"
                    @mouseover="$event.target.value = ''"
                    @mouseleave="$event.target.value = journalYear"
                    @input="datalistClick('year_field', 'years_list')"
                    :value="journalYear"
                    list="years_list"
                    class="date-selector__date"
                    :placeholder="journalYear"
                >
                <datalist id="years_list">
                    <option v-for="event in events" :value = event.title></option>
                </datalist>
            </div>
            <div v-else-if="journalType === 'equipment'" class="date-selector" data-toggle="tooltip" title="Выберите оборудование">
                <input id="equipment_field"
                    type="text"
                    @input="datalistClick('equipment_field', 'equipment_list')"
                    :value="journalEquipment"
                    @mouseover="$event.target.value = ''"
                    @mouseleave="$event.target.value = journalEquipment"
                    list="equipment_list"
                    class="date-selector__date"
                    :placeholder="journalEquipment"
                >
                <datalist id="equipment_list">
                    <option v-for="event in events" :value = event.title></option>
                </datalist>
            </div>
            <div v-else-if="journalType === 'month'" class="date-selector" data-toggle="tooltip" title="Выберите месяц">
                <input id="month_field"
                    type="text"
                    @input="datalistClick('month_field', 'month_list')"
                    :value="journalMonth + ' ' + journalYear"
                    @mouseover="$event.target.value = ''"
                    @mouseleave="$event.target.value = journalMonth + ' ' + journalYear"
                    list="month_list"
                    class="date-selector__date"
                    :placeholder="journalMonth + ' ' + journalYear"
                >
                <datalist id="month_list">
                    <option v-for="event in events" :value = event.month>{{event.year}}</option>
                </datalist>
            </div>

            <div class="panel-buttons">
                <div class="mode-buttons">
                    <span v-if="$store.getters['userState/isSuperuser'] || $store.getters['userState/isBoss']"
                         class="constraint_modes_button"
                    >
                        <button :class="{ 'btn--active':
                                mode=='edit_constraints', 'dropdown-toggle': true, 'btn': true}"
                                type="button"
                                id="dropdownMenuButton"
                                data-toggle="dropdown"
                                aria-haspopup="true"
                                aria-expanded="false"
                          >
                            <template v-if="mode=='edit_constraints' && $store.getters['journalState/currentConstraintsMode']">
                                {{ $store.getters['journalState/currentConstraintsMode'].message }}
                            </template>
                            <template v-else>
                                Ограничения полей
                            </template>
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">

                            <span v-for="mode in constraints_modes"
                                  class="dropdown-item-text"
                            >
                                <div class="input-group input-group-sm mb-3">
                                    <div class="input-group-prepend">
                                        <div class="input-group-text">
                                            <input :checked="$store.getters['journalState/constraintsModeIsActive'](mode.id)"
                                                   type="checkbox"
                                                   class="big-checkbox"
                                                   @click="toggleConstraintMode($event.target.checked, mode.id)"
                                            >
                                        </div>
                                    </div>
                                    <a @click="onConstraintsModeClick(mode.id)"
                                       type="text"
                                       class="form-control nav-link"
                                       style="background-color: #e9ecef"
                                       href="#"
                                    >
                                        {{ mode.message }}
                                    </a>
                                    <div class="input-group-append">
                                        <button class="btn"
                                                @click="deleteConstraintMode(mode.id)"
                                        >
                                        <i class="fa fa-trash" aria-hidden="true"></i>
                                            Удалить
                                        </button>
                                    </div>
                                </div>
                            </span>

                            <div class="dropdown-divider"></div>

                            <div class="dropdown-item-text"
                            >
                                <div class="input-group input-group-sm mb-3">
                                    <div class="input-group-prepend">
                                        <button class="btn"
                                                id="inputGroup-sizing-sm"
                                                @click="createConstraintMode()"
                                        >
                                            Добавить режим
                                        </button>
                                    </div>
                                    <input v-model="newConstraintModeMessage"
                                           type="text"
                                           placeholder="Введите название..."
                                           class="form-control"
                                           aria-label="Small"
                                           aria-describedby="inputGroup-sizing-sm"
                                    >
                                </div>
                            </div>
                        </div>
                    </span>

                    <template v-if="userHasPerm('edit') || $store.getters['userState/isSuperuser']">
                    <button :class="['btn', 'btn-edit', { 'btn--active': mode==='edit' }]"
                            @click="changeMode('edit')">
                        Редактирование
                    </button>
                    </template>

                    <template v-if="userHasPerm('validate') || $store.getters['userState/isSuperuser']">
                        <button :class="['btn', 'btn-validate', { 'btn--active': mode==='validate' }]"
                                @click="changeMode('validate')">
                            Валидация
                        </button>
                    </template>
                </div>
            </div>
        </div>
        <div v-if="journalType === 'shift'" class="responsibles">
          Ответственные за смену:
          <label v-for="employee of responsibles">
            <!-- <img style="height: 30px; width: 30px;" src="../assets/images/no-avatar.png"> -->
            {{ Object.values(employee)[0] }} &emsp;
          </label>
        </div>
    </div>
</template>
<script>
    import $ from 'jquery'
    import EventBus from '../EventBus'
    import ajax from '../axios.config'
    let XLSX = require('xlsx');

    export default {
        name: 'journal-panel',
        data() {
            return {
                showCalendar: false,
                employeeName: 'Employee name',
                employeePosition: 'position',
                newConstraintModeMessage: ''
            }
        },
        computed: {
            responsibles() {
                return this.$store.getters['journalState/journalInfo'].responsibles
            },
            userIsResponsible() {
                let responsibles = this.responsibles
                for (let i in responsibles) {
                    if (typeof responsibles[i][this.userName] != 'undefined') {
                        return true
                    }
                }
                return false
            },
            userName() {
                return this.$store.getters['userState/username']
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
            constraints_modes() {
                return this.$store.getters['journalState/constraintsModes']
            },
            shiftDate() {
                return this.$store.getters['journalState/journalInfo'].date;
            },
            shiftOrder() {
                return this.$store.getters['journalState/journalInfo'].order;
            },
            journalType() {
                return this.$store.getters['journalState/journalInfo'].journal.type;
            },
            journalYear() {
                return this.$store.getters['journalState/journalInfo'].year + '-й год';
            },
            journalMonth() {
                return this.$store.getters['journalState/journalInfo'].month;
            },
            journalEquipment() {
                return this.$store.getters['journalState/journalInfo'].equipment;
            },
        },
        methods: {
              createConstraintMode() {
                  var self = this
                  ajax.post(window.HOSTNAME+'/api/bl/modes_api/', {
                      message: self.newConstraintModeMessage,
                      plant: self.$store.getters['journalState/plantName'],
                      journal: self.$store.getters['journalState/journalName'],
                      fields: []
                  }, {
                      withCredentials: true
                  })
                  .then(function (response) {
                    self.$store.commit('journalState/ADD_CONSTRAINT', {
                        id: response.data.id,
                        message: self.newConstraintModeMessage,
                        is_active: false
                    });
                    self.$store.commit('journalState/SET_PAGE_MODE', 'edit_constraints')
                    self.$store.commit('journalState/SET_CONSTRAINTS_MODE', response.data.id)
                    this.newConstraintModeMessage = ''
                  })
                  .catch(e => {
                      console.log(e)
                  });
            },
            deleteConstraintMode(modeId) {
                this.$store.commit('journalState/DELETE_CONSTRAINTS_MODE', {id: modeId})
                ajax.delete(window.HOSTNAME+`/api/bl/modes_api/${modeId}`, {
                    withCredentials: true
                })
                .catch(e => {
                    console.log(e)
                });
            },
            toggleConstraintMode(checked, modeId) {
                this.$store.commit('journalState/TOGGLE_CONSTRAINTS_MODE', {id: modeId, active: checked})
                ajax.put(window.HOSTNAME+'/api/bl/modes_api/', { id: modeId, is_active: checked ? 1 : 0 }, {
                    withCredentials: true
                })
                .catch(e => {
                    console.log(e)
                });
            },
            onConstraintsModeClick (id) {
                this.$store.commit('journalState/SET_PAGE_MODE', 'edit_constraints')
                // begin editing chosen constraints mode
                this.$store.commit('journalState/SET_CONSTRAINTS_MODE', id)
            },
            onAgreeResponsibleClick () {
                this.$socket.sendObj({
                    'type': 'make_responsible',
                    'group_id': this.$store.getters['journalState/journalInfo'].id
                });
                this.$store.commit('journalState/SET_PAGE_MODE', 'edit')
                let payload = {}
                payload[this.$store.getters['userState/username']] = this.$store.getters['userState/username']
                this.$store.commit('journalState/ADD_RESPONSIBLE', payload)

                // let path = window.location.pathname;
                // if (path.slice(-1) !== '/'){path = path + '/'}
                // let shift_event = document.querySelector(`a[href='${path}'].fc-event`);
                // shift_event.setAttribute("style", "background-color:#169F85;border-color:#169F85");
            },
            userHasPerm(perm) {
                for (let p of this.$store.getters['journalState/journalInfo'].permissions.permissions) {
                    if (p == perm) {
                        return true
                    }
                }
              return false
            },
            removePerm(perm) {
                if (this.userHasPerm(perm)) {
                    this.$store.commit('journalState/REMOVE_PERMISSION', perm)
                }
            },
            changeMode(mode) {
                if (mode === 'edit') {
                    if ((!this.userIsResponsible) && (this.journalType === 'shift'))  {
                        EventBus.$emit('open-alert', {
                            onOk: this.onAgreeResponsibleClick,
                            text: 'Вы будете назначены ответственным за этот журнал после начала его редактирования'
                        })
                    }
                    else {
                        this.$store.commit('journalState/SET_PAGE_MODE', 'edit');
                    }
                }
                else {
                    this.$store.commit('journalState/SET_PAGE_MODE', mode);
                }
            },
            datalistClick(id, list) {
                let val = document.getElementById(id).value;
                let opts = document.getElementById(list).childNodes;
                let plantName = this.$route.params.plant;
                let journalName = this.$route.params.journal;
                for (let i = 0; i < opts.length; i++) {
                  if (opts[i].value === val) {
                      this.$store.dispatch('journalState/loadJournal', {
                          'id': this.events[i].id,
                          'plantName': plantName,
                          'journalName': journalName
                        })
                            .then(() => {
                                this.$router.push(this.events[i].url);

                            });
                    break;
                  }
                }
            },
            setListeners () {
                let self = this
                let journalTitleContainer = $(".journal_title_container");
                let lastScrollTop = 0;
                let startedScrollHeight = $(window).width() < 678 ? 400 : $(window).width() < 768 ? 200 : 100

                $(window).width() < 678 ? journalTitleContainer.css({'top': '94px'}) : null

                $(window).scroll(function(event){
                    let currentScrollTop = $(this).scrollTop();

                    if (currentScrollTop > $('.menu__panel').outerHeight() || $(window).width() >= 678) {
                        journalTitleContainer.css({'top': '50px'})

                        if(currentScrollTop < startedScrollHeight){
                            journalTitleContainer.removeClass("hidden").addClass("sticky")
                        }
                        if((lastScrollTop - currentScrollTop > 2) && (currentScrollTop > startedScrollHeight)) {
                            journalTitleContainer.removeClass("hidden").addClass("sticky");
                        } else if((currentScrollTop - lastScrollTop > 10) && (currentScrollTop > startedScrollHeight)) {
                            journalTitleContainer.removeClass("sticky").addClass("hidden");
                        }
                        lastScrollTop = currentScrollTop;
                    }
                    else {
                        journalTitleContainer.css({'top': (94 - currentScrollTop) + 'px'})
                        lastScrollTop = currentScrollTop;
                    }
                })
            },
            loadShifts () {
                this.$store.dispatch('journalState/loadShifts', {
                    plant: this.$route.params.plant,
                    journal: this.$route.params.journal
                })
            }
        },
        mounted() {
            let self = this;

            $('[data-toggle="tooltip"]').tooltip({delay: {show: 200, hide: 0}})

            setTimeout(() => this.loadShifts(), 0)

            this.setListeners()

            // $( window ).resize(function() {
            //     // console.log('resize')
            //     setTimeout(() => {
            //         $('.fc-scroller.fc-day-grid-container').css({'overflow': 'auto', 'height': '400px'})
            //     }, 100)
            // })
            //
            // $('.fc-toolbar.fc-header-toolbar button').click(function () {
            //     setTimeout(() => {
            //         $('.fc-scroller.fc-day-grid-container').css({'overflow': 'auto', 'height': '400px'})
            //     }, 1)
            // })
        }
    }
</script>
<style>
.big-checkbox {width: 16px; height: 16px;}
</style>
