var vueTest = new Vue({
  el: '#vue-test',
  // delimiters defines how to display vue variables in template: ${ var }
  delimiters: ['${', '}'],
  data: {
    plant_name: '',
    journal_name: '',
    tables: []
  },
  methods: {
    getTables: function () {
      console.log('http://127.0.0.1:8000/api/tables/?journal__plant__name=${this.plant_name}&journal__name=${journal_name}');
      axios
        .get('http://127.0.0.1:8000/api/tables/?journal__plant__name=${this.plant_name}&journal__name=${journal_name}')
        .then(response => {
          this.tables = response.data
        })
    }
  },
  mounted () {
    this.plant_name = window.location.pathname.split("/")[1];
    this.journal_name = window.location.pathname.split("/")[2];
    console.log('mounted!!!!!!!!!!!!!!!!!!!!!');
    this.getTables();
  }
});
