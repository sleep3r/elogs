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
                            <span class="message__info">{{message.type}}</span>
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
        <!-- <div class="loading" style="display: none;text-align: center">
            ЗАГРУЗКА...
        </div> -->
        <!--{% if page_obj.has_next %}-->
        <!-- <a class="infinite-more-link" href="?page={{ page_obj.next_page_number }}"></a> -->
        <!--{% endif %}-->
    </div>
</template>

<script>
    // import Waypoints from 'waypoints'

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
            setAsRead (id) {
                this.$store.dispatch('messagesState/readMessage', {id})
                    .then(() => {
                        this.$store.dispatch('messagesState/loadMessages')
                    })
            }
        },
        mounted() {
            this.$store.dispatch('messagesState/loadMessages')
            
            // let infinite = new Waypoint.Infinite({
            //     element: $('.messages__container')[0],
            //     onBeforePageLoad: function () {
            //         $('.loading').show();
            //     },
            //     onAfterPageLoad: function () {
            //         $('.loading').hide();
            //     },
            //     items: ".message",
            // });
        }
    }
</script>

<style scoped>

</style>