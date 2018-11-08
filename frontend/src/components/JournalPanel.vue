<template>
    <div class="journal__panel">
        <div class="shift-container">
            <div class="date-selector" data-toggle="tooltip" title="Выберите дату и смену">
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
            </div>
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

    export default {
        name: 'journal-panel',
        data() {
            return {
                showCalendar: false,
                employeeName: 'Employee name',
                employeePosition: 'position'
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
            shiftDate() {
                return this.$store.getters['journalState/journalInfo'].date;
            },
            shiftOrder() {
                return this.$store.getters['journalState/journalInfo'].order;
            },
        },
        methods: {
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
            setListeners () {
                let self = this
                let journalTitleContainer = $(".journal_title_container");
                let lastScrollTop = 0;
                let startedScrollHeight = $(window).width() < 678 ? 400 : $(window).width() < 768 ? 200 : 100

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

            $('[data-toggle="tooltip"]').tooltip({delay: {show: 200, hide: 0}})

            setTimeout(() => {
                this.$store.dispatch('journalState/loadShifts', {
                    plant: this.$route.params.plant,
                    journal: this.$route.params.journal
                }), 0
            })

            this.setListeners()

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
        }
    }
</script>
<style>

</style>
