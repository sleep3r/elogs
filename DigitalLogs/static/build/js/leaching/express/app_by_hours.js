
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

var appEA = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app_ea',
  data: {
    showModal: false,
    tables: {
        'form_template': {
            formId: 'form_template',
            data: [],
            current: {},
            current_count: 0,
            state: 'view',
            initRecord: {},
            init: function(scope){
                let form = document.getElementById(this.formId)
                var shiftId = form.shift_id.value
                scope.$http.get('/leaching/template?shift_id=' + shiftId)
                    .then(response => {
                        this.data = response.data
                        if (this.data.current_count > 1) {
                            this.state = 'edit'
                            this.current_count = this.data.current_count
                        } else {
                            this.state = 'add'
                            this.data = this.initRecord
                        }
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            saveRecord: function(scope) {
             console.log('save rocord')
                let form = document.getElementById(this.formId)
                let shiftId = form.shift_id.value
                let data = new FormData()
                data.append('shift_id', shiftId)
                data.append('items', JSON.stringify(this.data.items))
                scope.$http.post('/leaching/name/save', data)
                    .then(response => {
                        console.log(response.data)
                        this.state = 'edit'
                        this.init(scope)
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            addRecord: function(scope) {
              console.log('add rocord')
                let form = document.getElementById(this.formId)
                let shiftId = form.shift_id.value
                let data = new FormData()
                data.append('shift_id', shiftId)
                data.append('items', JSON.stringify(this.data.items))
                scope.$http.post('/leaching/name/add', data)
                    .then(response => {
                        console.log(response.data)
                        this.init(scope)
                        this.state = 'edit'
                    })
                    .catch(e => {
                        console.log(e)
                    })
            }
        },
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
                           context.rows.push({ hour: hour , info: response.data.items[hour] })
                     })
                     .catch(e => {
                        console.log(e)
                     })

                }

            }
        },
        'form_densers': {
            visible: 1,
            form_errors: [],
            data: [],
            rows: [],
            current: [],
            current_count: 0,
            initRecord: {},
            init: function(scope) {
                let formId = 'form_densers'
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                scope.getAnswerByUrl('/leaching/api/densers?shift_id=' + shiftId, formId)
            },
            onChange: function(scope) {
                formId = 'form_densers'
                let form = document.getElementById(formId)
                let hour = form.select_time.value
                let shiftId = form.shift_id.value

                scope.$http.get('/leaching/api/densers?shift_id=' + shiftId + '&hour=' + hour)
                    .then(response => {
                        this.current = response.data.items
                        this.current_count = response.data.count
                        this.init(scope)
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            saveRecord: function(scope) {
                let formId = 'form_densers'
                let form = document.getElementById(formId);
                let formData = new FormData(form)
                let formDataToSend = new FormData()

                formData.forEach((key, value) => {
                    formDataToSend.append(value,key)
                });

                scope.$http.post(form.action + '/json', formDataToSend)
                    .then(response => {
                        this.data = response.data
                        this.visible = 0
                        this.rows = []
                        this.current = this.initRecord
                        console.log(formId)
                    })
                    .catch(e => {
                        console.log(e)
                    })
            }
        },

    },
  },
  created: function() {
    this.tables['form_express_analysis'].init(this)
    // this.tables['form_densers'].init(this)
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
                this.tables[formId].data = response.data
                this.tables[formId].visible = 0
                this.tables[formId].rows = []
                console.log(formId)
            })
            .catch(e => {
                console.log(e)
            })
    },
    getAnswerByUrl: function(url, formId) {
        this.tables[formId].data = []

        this.$http.get(url)
            .then(response => {
                this.tables[formId].data = response.data
                console.info(this.tables[formId].data)
            })
            .catch(e => {
                console.log(e)
            })
    },
    getAnswerTo: function(url, scope) {
        this.$http.get(url)
            .then(response => {
                scope.current = response.data.items
                scope.current_count = response.data.count
                console.info(response.data)
            })
            .catch(e => {
                console.log(e)
            })
        console.log(url)
    },
    onChange: function(formId) {
        this.tables[formId].onChange(this)
    },
    onRemoveRow: function(rowId, formId) {
        this.tables[formId].onRemoveRow(this, rowId)
    },
    onRow: function(rowId, formId) {
        this.tables[formId].onRow(this, rowId)
    },
    saveRecord: function(formId) {
        console.log("save record")
        this.tables[formId].saveRecord(this)
    },
    addRecord: function(formId) {
        this.tables[formId].addRecord(this)
    },
    setAddState: function(formId) {
        this.tables[formId].state = 'add'
    }

  }
})