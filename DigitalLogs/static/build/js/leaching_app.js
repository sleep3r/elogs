
Vue.filter("formatNumber", function (value) {
    return numeral(value).format("00.00");
});

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('DD.MM.YYYY hh:mm')
  }
})

Vue.filter('formatHour', function(value) {
  if (value) {
    return moment(String(value)).format('hh')
  }
})

var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    showModal: false,
    tables: {
        'form_self_security': { visible: 1},
        'form_express_analysis': {
            visible: 1,
            rows: [],
            data: [],
            form_errors: [],
            init: function(scope) {

                let form = document.getElementById('form_express_analysis')
                var shiftId = form.shift_id.value

                scope.getAnswerByUrl('/leaching/api/express/analysis?shift_id='+ shiftId,'form_express_analysis' )
            },
            addNewRow: function(formId, scope) {
                let selectedTime = document.getElementById(formId+'_new_row_time');
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                var hour = selectedTime.value

                let obj = this.rows.find(x => x.hour === hour);
                if (this.rows.indexOf(obj) == -1) {


                    var context = this
                    scope.$http.get('/leaching/api/express/analysis?shift_id='+ shiftId + '&hour=' + hour)
                    .then(response => {
                        console.log('get hour')
                            console.log(response.data)
                           console.log(hour)
                           context.rows.push({ hour: hour , info: response.data.items[hour] })
                           console.info(context.rows)
                     })
                     .catch(e => {
                        console.log(e)
                     })

                }

            }
        },
    },
    posts: []
  },
  created: function() {
    this.tables['form_express_analysis'].init(this)
  },
  methods: {
    addNewRow: function(formId) {
        this.tables[formId].addNewRow(formId, this)
    },
    savePostForm: function(formId) {

        let form = document.getElementById(formId);
        let formData = new FormData(form)
        let formDataToSend = new FormData()

        formData.forEach((key, value) => {
            formDataToSend.append(value,key)
        });

        this.$http.post(form.action + '/json', formDataToSend)
                .then(response => {
                console.info(response.data)
                this.tables[formId].data = response.data
                this.tables[formId].visible = 0
                this.tables[formId].rows = []
        })
        .catch(e => {
            console.log(e)
        })

    },
    getAnswerByUrl: function(url, formId) {
        this.tables[formId].data = []

        this.$http.get(url)
            .then(response => {
                console.info('get from url: ' + url)
                console.log(formId)

                this.tables[formId].data = response.data
                console.info(this.tables[formId].data)


            })
            .catch(e => {
                console.log(e)
            })
    }

  }
})