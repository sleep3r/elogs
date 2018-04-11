var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#myModal',
    data: {
        answer: {}
    },
    created: function () {
        console.info('myModal.create')
        this.$http.get('leaching/shift/accessible')
            .then(response => {
                console.log(response.data);
                this.answer = response.data;
                init_calendar(response.data);
            })
            .catch(e => {
                console.log(e)
            })

        // calendar
        function init_calendar(shift_events) {

            if (typeof ($.fn.fullCalendar) === 'undefined') {
                return;
            }
            console.log('init_calendar');

            var date = new Date(),
                d = date.getDate(),
                m = date.getMonth(),
                y = date.getFullYear(),
                started,
                categoryClass;

            var calendar = $('#shift_calendar').fullCalendar({
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
                    right: 'month,agendaWeek,agendaDay,listMonth'
                },
                selectable: true,
                selectHelper: true,
                select: function (start, end, allDay) {
                    $('#fc_create').click();

                    started = start;
                    ended = end;

                    $(".antosubmit").on("click", function () {
                        var title = $("#title").val();
                        if (end) {
                            ended = end;
                        }

                        categoryClass = $("#event_type").val();

                        if (title) {
                            calendar.fullCalendar('renderEvent', {
                                    title: title,
                                    start: started,
                                    end: end,
                                    allDay: allDay
                                },
                                true // make the event "stick"
                            );
                        }

                        $('#title').val('');

                        calendar.fullCalendar('unselect');

                        $('.antoclose').click();

                        return false;
                    });
                },
                eventClick: function (calEvent, jsEvent, view) {
                    $('#fc_edit').click();
                    $('#title2').val(calEvent.title);

                    categoryClass = $("#event_type").val();

                    $(".antosubmit2").on("click", function () {
                        calEvent.title = $("#title2").val();

                        calendar.fullCalendar('updateEvent', calEvent);
                        $('.antoclose2').click();
                    });

                    calendar.fullCalendar('unselect');
                },
                editable: false,
                events: shift_events
            });

            calendar.fullCalendar('gotoDate', date);

        };
    }
})

function clickOnWizard() {
    console.log("click on Wizard");
    setTimeout(function(){
         $("button.fc-today-button").click()
    }, 500);

}