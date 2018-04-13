
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
  el: '#app_repair',
  baseLink: '/leaching/repair',
  data: {
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
        'form_repair': {
            formId: 'form_repair',
            data: [],
            current: {},
            editableId: 0,
            current_count: 0,
            state: 'view',
            initRecord: {},
            init: function(scope){
                scope.$http.get('/leaching/repair/allitems' )
                    .then(response => {
                        this.data = response.data
                        console.info(response.data)
                        this.current = Object.assign({}, this.initRecord)
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            onRow: function(scope, rowId) {
                console.log(rowId)
                this.editableId = rowId
            },
            saveRecord: function(scope) {
             console.log('save rocord')
                let data = new FormData()
                let recordToSave = this.data.items.filter( el => { return el.id === this.editableId })
                data.append('items', JSON.stringify(recordToSave))
                scope.$http.post(this.baseLink + '/save', data)
                    .then(response => {
                        console.log(response.data)
                        this.init(scope)
                        this.editableId = 0
                    })
                    .catch(e => {
                        console.log(e)
                    })
            },
            addRecord: function(scope) {
              console.log('add rocord')

                let data = new FormData()
                data.append('items', JSON.stringify(this.current))
                scope.$http.post(this.baseLink + '/add', data)
                    .then(response => {
                        console.log(response.data)
                        this.init(scope)
                        this.current = Object.assign({}, this.initRecord)
                    })
                    .catch(e => {
                        console.log(e)
                    })

            }
        },
    },
  },
  created: function() {
    this.tables['form_repair'].init(this)
  },
  methods: {
    addNewRow: function(formId) {
        this.tables[formId].addNewRow(formId, this)
    },
    onChange: function(formId) {
        this.tables[formId].onChange(this)
    },
    onRemoveRow: function(rowId, formId) {
        console.log(formId + '' + rowId)
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