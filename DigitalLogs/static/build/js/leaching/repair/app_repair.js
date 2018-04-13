
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

  data: {
    baseLink: '/leaching/repair',
    resource_url: '/leaching/repair/allitems',
    tables: {
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
                let data = new FormData()
                let recordToSave = this.data.items.filter( el => { return el.id === this.editableId })
                data.append('items', JSON.stringify(recordToSave))
                scope.$http.post(scope.baseLink + '/save', data)
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
                let data = new FormData()
                data.append('items', JSON.stringify(this.current))
                scope.$http.post(scope.baseLink + '/add', data)
                    .then(response => {
                        console.log(response.data)
                        this.init(scope)
                        this.current = Object.assign({}, this.initRecord)
                    })
                    .catch(e => {
                        console.log(e)
                    })

            },
            removeRecord: function(scope, rowId) {
                console.log(scope.baseLink)
                scope.$http.get(scope.baseLink + '/remove?id='+rowId)
                    .then( response => {
                        this.init(scope)
                    })
                    .catch( e => {
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
    updateResource(data) {
        this.data = data
    },
    addNewRow: function(formId) {
        this.tables[formId].addNewRow(formId, this)
    },
    onChange: function(formId) {
        this.tables[formId].onChange(this)
    },
    removeRecord: function(rowId, formId) {
        console.log(formId + ' ' + rowId)
        this.tables[formId].removeRecord(this, rowId)
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