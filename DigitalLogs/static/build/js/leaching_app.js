
var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    showModal: false,
    message: 'Hello Vue!',
    posts: []
  },
  methods: {
    reverseMessage: function () {
      this.message = this.message.split('').reverse().join('')

    },
    savePostForm: function(formId) {
        let form = document.getElementById(formId);
        console.log(form.action)
        console.info(JSON.stringify(form))
        let formData = new FormData(form)

        data = []

        formData.forEach((key, value) => {
            data[value] = key;
        });

        console.info(data)

        axios({
            method: 'post',
            url: '/json/densers',
  data: {
    firstName: 'Fred',
    lastName: 'Flintstone'
  }
});

//        axios.post(form.action + '/json', {
        axios.post('/json/densers', data)
        .then(response => {
            console.info(response.data)
        })
        .catch(e => {
            console.log(e)
        })

        console.info("save")
        console.info(formId)


    }
  }
})