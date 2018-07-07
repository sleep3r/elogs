<template>
  <div>
  <li class="notification" v-bind:data-message="item.text" v-bind:data-id="item.id" v-for="item, key in items">
        <a href="javascript:;" onclick="return Notifications.open(event, this)">
            <div class="notification-icon">
                <i v-if="item.type === 'comment' " class="material-icons" style="font-size:24px; color: #669900;" >announcement</i>
                <i v-else-if="item.type === 'critical_value' " class="material-icons" style="font-size:24px; color: #FF0000;" >new_releases</i>
            </div>
            <div class="notification-text">
                <p v-html="item.text"></p>
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
    this.timer = setInterval(this.getMessages, 9000)
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