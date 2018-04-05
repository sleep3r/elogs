
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
        'form_self_security': {
            formId: 'form_self_security',
            data: [],
            current: {},
            current_count: 0,
            state: 'view',
            initRecord: { 'items': {'bignote':'', 'notes': { '0':{}, '1':{}, '2':{}}}},
            init: function(scope){
                let form = document.getElementById(this.formId)
                var shiftId = form.shift_id.value
                scope.$http.get('/leaching/self/security?shift_id=' + shiftId)
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
                scope.$http.post('/leaching/self/security/save', data)
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
                scope.$http.post('/leaching/self/security/add', data)
                    .then(response => {
                        console.log(response.data)
                        this.init(scope)
                        this.state = 'edit'

                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
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
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
             onRow: function(scope, rowId) {
                this.state = 'edit'
                this.current = this.data.items[rowId]
            },
            onRemoveRow: function(scope, rowId) {
                let mans = [1, 4]
                mans.forEach( manNumber => {
                    if (this.data.items[rowId][manNumber]){
                         let recordId = this.data.items[rowId][manNumber]['id']
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
                let formId = 'form_hydrometal'
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                let data = new FormData()
                this.newRecord['shift_id'] = shiftId
                this.newRecord['extra'] = this.data['extra']
                data.append('item', JSON.stringify(this.newRecord))
                scope.$http.post('leaching/update/hydrometal', data)
                    .then(response => {
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
                let formId = 'form_pulps'
                let form = document.getElementById(formId)
                let shiftId = form.shift_id.value
                this.current = this.data.items[rowId]
            },
            onRemoveRow: function(scope, rowId) {
                let recordId = rowId
                scope.$http.get('/leaching/api/pulps/remove?combid=' + recordId)
                     .then(response => {
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
                        this.state = 'view'
                        this.current = {'zn_pulp':{}, 'cu_pulp':{}, 'fe_sol':{}}
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            addRecord: function(scope) {
                let formId = 'form_pulps'
                let form = document.getElementById(formId)
                var shiftId = form.shift_id.value
                let data = new FormData()
                this.newRecord['shift_id'] = shiftId
                this.newRecord['extra'] = this.data['extra']
                data.append('item', JSON.stringify(this.newRecord))
                scope.$http.post('leaching/update/pulps', data)
                    .then(response => {
                        this.state = 'view'
                        this.init(scope)
                        this.newRecord = {'zn_pulp':{}, 'cu_pulp':{}, 'fe_sol':{}, 'extra': {}}
                    })
                    .catch(e => {
                        console.log(e)
                    })
            }
        },
        'form_agitators': {
            data: [],
            formId: 'form_agitators',
            initRecord: {'times':[ { '13':{ 'true':{}, 'false':{} }, '15':{ 'true':{}, 'false':{} }, '17':{ 'true':{}, 'false':{} }, '19':{ 'true':{}, 'false':{} }},
                { '13':{ 'true':{}, 'false':{} }, '15':{ 'true':{}, 'false':{} }, '17':{ 'true':{}, 'false':{} }, '19':{ 'true':{}, 'false':{} }},
                { '13':{ 'true':{}, 'false':{} }, '15':{ 'true':{}, 'false':{} }, '17':{ 'true':{}, 'false':{} }, '19':{ 'true':{}, 'false':{} }},
            ], 'comment': ''},
            current: {},
            current_count: 0,
            state: 'view',
            newRecord: {},
            init: function(scope){
               let formId = 'form_agitators'
               let form = document.getElementById(formId)
               let shiftId = form.shift_id.value
               scope.$http.get('leaching/api/agitators?shift_id=' + shiftId)
                    .then(response => {
                        this.state = 'view'
                        this.data = response.data
                        if (this.data.items.times) {
                            this.current = this.initRecord
                            this.state = 'edit'
                        } else {
                            this.newRecord = this.initRecord
                            this.state = 'add'
                        }

                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            onRemoveRow: function(scope, rowId) {
            },
            onRow: function(scope, rowId) {
            },
            saveRecord: function(scope) {
                let form = document.getElementById(this.formId)
                let shiftId = form.shift_id.value
                let data = new FormData()
                data.append('shift_id', shiftId)
                data.append('items', JSON.stringify(this.data.items))

                scope.$http.post('/leaching/agitators/update', data)
                    .then(response => {
                        this.state = 'edit'

                        this.newRecord = this.initRecord
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            addRecord: function(scope) {
                let form = document.getElementById(this.formId)
                let shiftId = form.shift_id.value
                let data = new FormData()
                data.append('shift_id', shiftId)
                data.append('items', JSON.stringify(this.newRecord))
                data.append('comment', this.data.items.comment)
                scope.$http.post('/leaching/agitators/add', data)
                    .then(response => {
                        console.log(response.data)
                        this.state = 'add'
                        this.newRecord = this.initRecord
                    })
                    .catch(e => {
                        console.log(e)
                    })
            }
        },
        'form_cinder': {
            formId: 'form_cinder',
            data: [],
            current: {},
            current_count: 0,
            state: 'add',
            initRecord: {'items': {'0':{ 'shift_total':0,'day_total':0, 'in_process':0}, '1': { 'shift_total':0,'day_total':0, 'in_process':0}} },
            init: function(scope){
                console.info(this.formId)
                let form = document.getElementById(this.formId)
                var shiftId = form.shift_id.value
                scope.$http.get('/leaching/cinder?shift_id='+ shiftId)
                    .then(response => {
                        this.current_count = response.data.current_count
                        this.data = response.data

                        if (this.current_count > 0) {
                            this.state = 'edit'
                        } else {
                            this.state = 'add'
                            this.data = this.initRecord
                        }

                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            onRemoveRow: function(scope, rowId) {
            },
            onRow: function(scope, rowId) {
            },
            saveRecord: function(scope) {
                let form = document.getElementById(this.formId)
                let shiftId = form.shift_id.value
                let data = new FormData()
                data.append('shift_id', shiftId)
                data.append('items', JSON.stringify(this.data.items))

                scope.$http.post('/leaching/cinder/save', data)
                    .then(response => {
                        this.state = 'edit'
                        this.init(scope)
                    })
                    .catch(e => {
                        console.error(e)
                    })
            },
            addRecord: function(scope) {
                let form = document.getElementById(this.formId)
                let shiftId = form.shift_id.value
                let data = new FormData()
                data.append('shift_id', shiftId)
                data.append('items', JSON.stringify(this.data.items))

                scope.$http.post('/leaching/cinder/add', data)
                    .then(response => {
                        this.state = 'edit'
                        this.init(scope)

                    })
                    .catch(e => {
                        console.log(e)
                    })
            }
        },
        'form_reagents': {
            formId: 'form_reagents',
            data: [],
            current: {},
            current_count: 0,
            state: 'view',
            initRecord: {'items': {
                'states':{
                    'delivered': {},
                    'taken': {},
                    'consumption': {},
                    'issued': {}
                  },
                'fence_state': '',
                'stages_zn_dust':{'1st':0,'2st':0,'3st':0,'cd':0} }},
            init: function(scope){
                let form = document.getElementById(this.formId)
                var shiftId = form.shift_id.value
                scope.$http.get('/leaching/reagents?shift_id=' + shiftId)
                    .then(response => {
                        this.data = response.data
                        console.info("reagents")
                        console.info(this.data)
                        if (this.data.current_count > 1) {
                            this.state = 'edit'
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

                scope.$http.post('/leaching/reagents/save', data)
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
                scope.$http.post('/leaching/reagents/add', data)
                    .then(response => {
                        console.log(response.data)
                        this.init(scope)
                    })
                    .catch(e => {
                        console.log(e)
                    })
            }
        },
        'form_ready_tanks': {
            formId: 'form_ready_tanks',
            data: [],
            current: {},
            current_count: 0,
            state: 'view',
            initRecord: {'items':{'3':{'num':3}, '4':{'num':4}, '5':{'num':5}}},
            init: function(scope){
                let form = document.getElementById(this.formId)
                var shiftId = form.shift_id.value
                scope.$http.get('/leaching/ready/tanks?shift_id=' + shiftId)
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
            onRemoveRow: function(scope, rowId) {
            },
            onRow: function(scope, rowId) {
            },
            saveRecord: function(scope) {
             console.log('save rocord')
                let form = document.getElementById(this.formId)
                let shiftId = form.shift_id.value
                let data = new FormData()
                data.append('shift_id', shiftId)
                data.append('items', JSON.stringify(this.data.items))
                scope.$http.post('/leaching/ready/tanks/save', data)
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
                scope.$http.post('/leaching/ready/tanks/add', data)
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
        'form_neutural_solution': {
            formId: 'form_neutural_solution',
            data: [],
            current: {},
            current_count: 0,
            state: 'edit',
            initRecord: { 'items': {'0':{}, '1':{}, '2':{}, '3':{}, '4':{}, '5':{}, '6':{}, '7':{}, '8':{} }},
            init: function(scope){
                let form = document.getElementById(this.formId)
                var shiftId = form.shift_id.value
                scope.$http.get('/leaching/neutural/solution?shift_id=' + shiftId)
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
                scope.$http.post('/leaching/neutural/solution/save', data)
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
                scope.$http.post('/leaching/neutural/solution/add', data)
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
        'form_empty_tanks': {
            formId: 'form_empty_tanks',
            data: [],
            current: {},
            current_count: 0,
            state: 'view',
            initRecord: {'items': {
                '0':{'tank_name':'Бак отработ. 1-2 серий'},
                '1':{'tank_name':'Манны №1-9'},
                '2':{'tank_name':'Манны ВТВ №10-12'},
                '3':{'tank_name':'Обор-й сгуститель №9'},
                '4':{'tank_name':'Агитатор 22'},
                '5':{'tank_name':'Бак нейтр. р-ра, 1-й цех'},
                '6':{'tank_name':'Ман отраб. № 2, 1-й цех'},
                '7':{'tank_name':'Ман отраб. № 3, 1-й цех'},
                '8':{'tank_name':'Ман отраб. № 9, 1-й цех'},
                '9':{'tank_name':'-'},
                '10':{'tank_name':'СМЕННЫЙ БАЛАНС'},
                '11':{'tank_name':'СУТОЧНЫЙ БАЛАНС'},
                }
            },
            init: function(scope){
                let form = document.getElementById(this.formId)
                var shiftId = form.shift_id.value
                scope.$http.get('/leaching/empty/tanks?shift_id=' + shiftId)
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
                scope.$http.post('/leaching/empty/tanks/save', data)
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
                scope.$http.post('/leaching/empty/tanks/add', data)
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
    },
  },
  created: function() {
    this.tables['form_express_analysis'].init(this)
    this.tables['form_densers'].init(this)
    this.tables['form_hydrometal'].init(this)
    this.tables['form_pulps'].init(this)
    this.tables['form_agitators'].init(this)
    this.tables['form_cinder'].init(this)
    this.tables['form_reagents'].init(this)
    this.tables['form_ready_tanks'].init(this)
    this.tables['form_neutural_solution'].init(this)
    this.tables['form_self_security'].init(this)
    this.tables['form_empty_tanks'].init(this)
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