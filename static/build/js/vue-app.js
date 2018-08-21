
Vue.component('cell', {
  props: ['field_name'],
  template: '<div><p>{this.props.field_name}</p><input type="text" name="field_name" v-model="field_name" /></div>'
})

var elogsApp = new Vue({
  el: '#elogs-app',
  delimiters: ['%{', '}'],
  data: {
    plant_name: '',
    journal_name: '',
    tables: []
  },
  methods: {
    getTables: function () {
      axios
        .get('/api/tables/?journal__plant__name='+this.plant_name+'&journal__name='+this.journal_name)
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
