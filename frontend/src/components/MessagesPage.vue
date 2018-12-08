<template>
    <div class="messages">
        <ul class="messages__list">
            <h1 v-if="!getMessages.length" style="text-align: center">Нет сообщений</h1>
            <div class="messages__container" v-else>
                <h4>Сообщения</h4>
                <li class="message" v-for="message in getMessages" :key="message.id">
                    <div v-if="message.sendee" class="message__title__container">
                        <img class="message__image" src="../assets/images/no-avatar.png">
                        <!-- <span class="message__author-name">{{ message.user_name }}</span> -->
                        <strong class="message__title">
                            <span class="sendee">{{message.sendee}}</span>
                        </strong>
                        <strong class="message__title">
                            <span class="message__info">{{ messageTypeText(message) }}</span>
                        </strong>
                        <strong class="message__title">
                            <a :href="message.link">{{message.cell ? message.cell.field.name : null}}</a>
                        </strong>
                    </div>
                    <template>
                        <p :class="['message__text', message.type]">{{message.text}}</p>
                        <span class="message__created">{{new Date(message.created).toLocaleString()}}</span>
                    </template>
                    <div class="message__is-read" v-if="!message.is_read" @click="setAsRead(message.id)"></div>
                </li>
            </div>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "MessagesPage",
        data() {
            return {

            }
        },
        computed: {
            getMessages () {
                return this.$store.getters['messagesState/messages']
            }
        },
        methods: {
            messageTypeText (message) {
              switch (message.type) {
                  case 'set_mode':
                      return 'Установлен режим'
                  case 'critical_value':
                      return 'Критическое значение'
                  case 'comment':
                      return 'Комментарий к ячейке'
                  default:
                      return ''
                }
            },
            setAsRead (id) {
                this.$store.dispatch('messagesState/readMessage', {id})
                    .then(() => {
                        this.$store.dispatch('messagesState/loadMessages')
                    })
            }
        },
        mounted() {
            this.$store.dispatch('messagesState/loadMessages')
        }
    }
</script>

<style scoped>

</style>
