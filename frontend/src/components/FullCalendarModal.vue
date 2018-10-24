<template>
    <div class="modal fade" id="FullCalendarModal" tabindex="-1" role="dialog" aria-labelledby="FullCalendarModal" aria-hidden="true">
        <div class="modal-dialog modal-dialog-large" role="document">
            <div class="modal-content modal-content-large">
                <div class="modal-body">
                    <full-calendar :events="events" :config="fullCalendarConfig" ref="calendar"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {FullCalendar} from 'vue-full-calendar'

    export default {
        name: "FullCalendarModal",
        data () {
            return {
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
                        // console.log("event click");
                    },
                    editable: false,
                }
            }
        },
        computed: {
            events() {
                return this.$store.getters['journalState/events'];
            }
        },
        methods: {
            
        },
        mounted () {
            
        },
        components: {
            FullCalendar
        },
    }
</script>

<style scoped>
    @media (min-width: 576px) {
        #FullCalendarModal .modal-dialog {
            max-width: 90%;
        }
    }
</style>