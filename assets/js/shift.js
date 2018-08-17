var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#modal_shift',
    data: {
        answer: {}
    },
    created: function () {
        let plant = location.pathname.split('/')[1];
        let journal_name = location.pathname.split('/')[2];

        if (!plant || !journal_name) {
            plant = 'furnace';
            journal_name = 'fractional';
        }


        this.$http.get('/' + plant + '/' + journal_name +'/get_shifts')
            .then(response => {
                this.answer = response.data;
                init_calendar(response.data);
            })
            .catch(e => {
                console.log(e)
            });

        // calendar
        function init_calendar(shift_events) {

            if (typeof ($.fn.fullCalendar) === 'undefined') {
                return;
            }

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

            //calendar.fullCalendar('gotoDate', date);

        };
    }
})


class Shift {

    static showCalendar() {
        let modal = document.querySelector("#modal_shift");
        modal.style.display = 'block';
        $('#shift_calendar').fullCalendar('render');
    }

    static close() {
        let modalWindow = document.getElementById("modal_shift");
        modalWindow.style.display = "none";
    }

    static confirm() {
        let edit = $("input[name='edit']").attr("value");
        if (edit === "True") {
            let has_edited = $("input[name='has_edited']").attr("value");
            if (!(has_edited === "True")) {
                $.confirm({
                    title: 'Продолжить?',
                    content: 'Вы будете назначены отвественным за этот журнал',
                    autoClose: 'cancel|60000',
                    theme: 'supervan',
                    buttons: {
                        confirm: {
                            text: "Да",
                            action: function() {$("form").trigger("input")}
                        },
                        cancel: {
                            text: "Назад",
                            action: function () {
                                history.back();
                            },
                        }
                    }
                });
            }
        }
    }

}
