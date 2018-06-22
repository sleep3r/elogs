<template>
  <div>
  <li class="notification" v-bind:data-message="item.text" v-bind:data-id="item.id" v-for="item, key in items">
        <a href="javascript:;" onclick="return Notifications.open(event, this)">
                <div class="notification__number">
                    <span class="badge badge-secondary">{{item.id}}</span>
                </div>
                <div class="notification-icon">
                    <img v-bind:src="'/static/images/notif/' + item.type + '.png'">
                </div>
                <div class="notification-text">
                    <p>
                        {{item.text}}
                    </p>
                </div>
        </a>
  </li>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Messages',
  data() {
    return {
        items: [],
        errors: []
     }
  },

  created() {
    this.getMessages()
    this.timer = setInterval(this.getMessages, 55000)
  },
  methods: {
    getMessages() {
        axios.get('/common/messages/get')
            .then(({ data }) => {
                this.items = data.messages
                let counter = document.getElementById("notifications_count")
                counter.innerHTML = Object.keys(data.messages).length
            })
            .catch(e => {
                this.errors.push(e)
            })
    }

  }
}
</script>