
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

Vue.component('my-component', {
  template: '<div><b>Пользовательский компонент!<b></div>'
})


var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    showModal: false,
    tables: {
        'form_template': {
            data: [],
            current: [],
            current_count: 0,
            state: 'view',
            newRecord: {},
            init: function(scope){
            },

        },
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
        'form_densers': {
            visible: 1,
            form_errors: [],
            data: [],
            rows: [],
            current: [],
            current_count: 0,
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

                scope.getAnswerTo('/leaching/api/densers?shift_id=' + shiftId + '&hour=' + hour, this )

            }
        },
        'form_hydrometal': {
            visible: 1,
            data: [],
            current: [],
            current_count: 0,
            newRecord: {'1':{},'4':{},'extra':{'fe_avg':123,'fe_shave':999}},
            state: 'view',
            init: function(scope) {
                let formId = 'form_hydrometal'
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                this.data = []

                scope.$http.get('/leaching/api/hydrometal?shift_id=' + shiftId)
                    .then(response => {
                        this.data = response.data
                        console.info(this.data)
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            onRow: function(scope, rowId) {
                this.state = 'edit'
                console.log(rowId)
                console.log(this.data.items[rowId])
                this.current = this.data.items[rowId]
            },
            onRemoveRow: function(scope, rowId) {
                let mans = [1, 4]
                mans.forEach( manNumber => {
                    console.log(manNumber)
                    if (this.data.items[rowId][manNumber]){
                         let recordId = this.data.items[rowId][manNumber]['id']
                         console.log(recordId)
                         scope.$http.get('/leaching/api/hydrometal/remove?id=' + recordId)
                            .then(response => {
                                console.info(response.data)
                                Vue.delete(this.data.items, rowId)
                            })
                            .catch(e => {
                                console.log(e)
                            })
                    }
                })
            },
            addRecord: function(scope) {
                console.log("add record")
                let formId = 'form_hydrometal'
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                let data = new FormData()
                this.newRecord['shift_id'] = shiftId
                this.newRecord['extra'] = this.data['extra']
                data.append('item', JSON.stringify(this.newRecord))
                scope.$http.post('leaching/update/hydrometal', data)
                    .then(response => {
                        console.log(response.data)
                        this.state = 'view'
                        this.init(scope)
                        this.newRecord = {'1':{},'4':{},'extra':{ }}
                    })
                    .catch(e => {
                        console.log(e)
                    })
            }
        },
        'form_pulps': {
            data: [],
            current: {'zn_pulp':{}, 'cu_pulp':{}, 'fe_sol':{}, 'extra': {}},
            current_count: 0,
            state: 'view',
            newRecord: {'zn_pulp':{}, 'cu_pulp':{}, 'fe_sol':{}, 'extra': {}},
            init: function(scope){
                let formId = 'form_pulps'
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                scope.$http.get('/leaching/api/pulps?shift_id='+ shiftId)
                    .then(response => {
                        console.info('form_pulps.init')
                        console.info(response.data);
                        if (this.data.items) {
                            setTimeout(() => {
                                let datarows = document.querySelectorAll("#form_pulps tbody tr.mini")
                                datarows[datarows.length - 1].className += " add-row-animated"
                            }, 0);
                        }
                        this.data = response.data
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            onRow: function(scope, rowId) {
                this.state = 'edit'
                console.log(rowId)
                let formId = 'form_pulps'
                let form = document.getElementById(formId)
                let shiftId = form.shift_id.value
                console.log(this.data.items[rowId])
                this.current = this.data.items[rowId]
            },
            onRemoveRow: function(scope, rowId) {
                let recordId = rowId
                console.log(recordId)
                scope.$http.get('/leaching/api/pulps/remove?combid=' + recordId)
                     .then(response => {
                          console.info(response.data)
                          Vue.delete(this.data.items, rowId)
                     })
                     .catch(e => {
                          console.log(e)
                     })
            },
            saveRecord: function(scope) {
                let formId = 'form_pulps'
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                let data = new FormData()
                this.current['shift_id'] = shiftId
                this.current['extra'] = this.data['extra']
                data.append('item', JSON.stringify(this.current))
                scope.$http.post('leaching/update/pulps', data)
                    .then(response => {
                        console.log(response.data)
                        this.state = 'view'
                        this.current = {'zn_pulp':{}, 'cu_pulp':{}, 'fe_sol':{}}
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            addRecord: function(scope) {

                console.info("add new Record")
                let formId = 'form_pulps'
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                let data = new FormData()
                this.newRecord['shift_id'] = shiftId
                this.newRecord['extra'] = this.data['extra']
                data.append('item', JSON.stringify(this.newRecord))
                scope.$http.post('leaching/update/pulps', data)
                    .then(response => {
                        console.log(response.data)
                        this.state = 'view'
                        this.init(scope)
                        this.newRecord = {'zn_pulp':{}, 'cu_pulp':{}, 'fe_sol':{}, 'extra': {}}
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
    this.tables['form_densers'].init(this)
    this.tables['form_hydrometal'].init(this)
    this.tables['form_pulps'].init(this)
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
    saveRow: function(formId) {
        console.log("save row -> " +formId )

        let data = new FormData()
        data.append('item', JSON.stringify(this.tables[formId].current))

        this.$http.post('leaching/update/hydrometal', data)
            .then(response => {
                console.log(response.data)
                this.tables[formId].current = null
            })
            .catch(e => {
                console.log(e)
            })

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