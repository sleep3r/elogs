

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
    message: 'Hello Vue!',
    tables: {
        'form_self_security': { visible: 1
        }
    },
    posts: []
  },
  methods: {
    reverseMessage: function () {
      this.message = this.message.split('').reverse().join('')

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
        })
        .catch(e => {
            console.log(e)
        })

    }
  }
})