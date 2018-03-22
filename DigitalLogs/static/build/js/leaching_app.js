Vue.component('modal', {
  template: '#modal-template'
})

var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    showModal: false,
    message: 'Hello Vue!'
  },
  methods: {
    reverseMessage: function () {
      this.message = this.message.split('').reverse().join('')
    }
  }
})