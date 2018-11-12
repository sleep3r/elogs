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
                   data-target="#FullCalendarModal"
            >
        </div>
        <div class="panel-buttons">

            <div v-if="$store.getters['userState/isSuperuser'] || $store.getters['userState/isBoss']"
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
            </div>

            <div class="mode-buttons">
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
            <button :class="['btn', 'btn-xlsx', 'float-right']"
                    @click="download_xlsx()">
                XLSX
            </button>
        </div>
        <div class="exp-time">
          <span> {{ shiftMessage }} </span>
        </div>
        <div class="responsibles">
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
                now: new Date(),
                shiftMessage: '',
                showCalendar: false,
                employeeName: 'Employee name',
                employeePosition: 'position',
                newConstraintModeMessage: ''
            }
        },
        watch: {
            now (value) {
                this.updateShiftMode();
            },
        },
        computed: {
            remainingTime() {
                // time before shift editing will be closed
                let deadline
                if (this.userIsResponsible) {
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
                return Date.parse(this.timeLimits['editing_mode_closing'])
            },
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

                let path = window.location.pathname;
                if (path.slice(-1) !== '/'){path = path + '/'}
                let shift_event = document.querySelector(`a[href='${path}'].fc-event`);
                shift_event.setAttribute("style", "background-color:#169F85;border-color:#169F85");
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
                    if (!this.userIsResponsible) {
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
            updateShiftMode() {
                if (((!this.timeLimits) && this.userHasPerm('edit')) || this.$store.getters['userState/isSuperuser']) {
                    this.shiftMessage = 'Смена открыта для редактирования'
                }
                else if ((!this.userHasPerm('edit'))) {
                    this.shiftMessage = 'Вы не можете редактировать эту смену'
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
            },
            setListeners () {
                let self = this
                let journalTitleContainer = $(".journal_title_container");
                let lastScrollTop = 0;
                let startedScrollHeight = $(window).width() < 678 ? 400 : $(window).width() < 1012 ? 200 : 100

                $(window).scroll(function(event){
                    let currentScrollTop = $(this).scrollTop();
                    if(currentScrollTop < startedScrollHeight){
                        journalTitleContainer.removeClass("hidden").addClass("sticky")
                    }
                    if((lastScrollTop - currentScrollTop > 2) && (currentScrollTop > startedScrollHeight)) {
                        journalTitleContainer.removeClass("hidden").addClass("sticky");
                    } else if((currentScrollTop - lastScrollTop > 10) && (currentScrollTop > startedScrollHeight)) {
                        journalTitleContainer.removeClass("sticky").addClass("hidden");
                    }
                    lastScrollTop = currentScrollTop;
                });
            }
        },
        mounted() {
            let self = this;

            setTimeout(() => {
                this.$store.dispatch('journalState/loadShifts', {
                    plant: this.$route.params.plant,
                    journal: this.$route.params.journal
                }), 0
            })

            this.setListeners()

            this.updateShiftMode()

            $( window ).resize(function() {
                // console.log('resize')
                setTimeout(() => {
                    $('.fc-scroller.fc-day-grid-container').css({'overflow': 'auto', 'height': '400px'})
                }, 100)
            })

            $('.fc-toolbar.fc-header-toolbar button').click(function () {
                setTimeout(() => {
                    $('.fc-scroller.fc-day-grid-container').css({'overflow': 'auto', 'height': '400px'})
                }, 1)
            })

            // if (this.userIsResponsible) {
            //     console.log('awdawd')
            // }
        },
        created() {
            setInterval(() => this.now = (new Date()).getTime(), 1000)
        }
    }
</script>
<style>
.big-checkbox {width: 16px; height: 16px;}
</style>
