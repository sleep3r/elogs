
Vue.component('cell', {
  props: ['field_name'],
  template: '<input>{{ field_name }}</input>'
})

var elogsApp = new Vue({
  el: '#elogs-app',
  // delimiters defines template syntax for variables: ${ var }
  delimiters: ['${', '}'],
  data: {
    plant_name: '',
    journal_name: '',
    tables: []
  },
  methods: {
    getTables: function () {
      axios
        .get('http://127.0.0.1:8000/api/tables/?journal__plant__name='+this.plant_name+'&journal__name='+this.journal_name)
        .then(response => {
          this.tables = response.data
        })
    }
  },
  mounted () {
    this.plant_name = window.location.pathname.split("/")[1];
    this.journal_name = window.location.pathname.split("/")[2];
    this.getTables();
  }
});
