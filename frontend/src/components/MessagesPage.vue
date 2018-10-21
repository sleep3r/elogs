<template>
    <div class="messages">
        <ul class="messages__list">
            <h1 v-if="!messages.length" style="text-align: center">Нет сообщений</h1>
            <template v-else>
                <li class="message" v-for="message in messages" :key="message.id">
                    <template v-if="message.sendee">
                        <img class="message__image" src="../assets/images/no-avatar.png">
                        <span class="message__author-name">{{ message.user_name }}</span>
                        <strong class="message__title">
                            <a class="sendee" href="#">{{message.sendee}}</a>
                            <span class="message__info"></span>
                            <a :href="message.link">{{message.cell.field.name}}</a>
                        </strong>
                    </template>
                    <template v-else>
                        <p :class="['message__text', message.type]">{{message.text}}</p>
                        <span class="message__created">{{message.created}}</span>
                    </template>
                </li>
            </template>
        </ul>
        <div class="loading" style="display: none;text-align: center">
            ЗАГРУЗКА...
        </div>
        <!--{% if page_obj.has_next %}-->
        <!--<a class="infinite-more-link" href="?page={{ page_obj.next_page_number }}"></a>-->
        <!--{% endif %}-->
    </div>
</template>

<script>
    // import Waypoints from 'waypoints'

    export default {
        name: "MessagesPage",
        data() {
            return {
                messages: [
                    // {
                    //     id: 1,
                    //     user_name: 'dfsfs',
                    //     sendee: 'esdad',
                    //     link: 'dadsasd',
                    //     cell: {
                    //         field: {
                    //             name: 'csadas'
                    //         }
                    //     },
                    //     type: 'dsa',
                    //     text: 'sadas',
                    //     created:'dasdad'
                    // },
                    // {
                    //     id: 2,
                    //     user_name: 'dfsfs',
                    //     sendee: 'esdad',
                    //     link: 'dadsasd',
                    //     cell: {
                    //         field: {
                    //             name: 'csadas'
                    //         }
                    //     },
                    //     type: 'dsa',
                    //     text: 'sadas',
                    //     created:'dasdad'
                    // }
                ]
            }
        },
        mounted() {
            this.$store.dispatch('messagesState/loadMessages')
            
            // let infinite = new Waypoint.Infinite({
            //     element: $('.notifs')[0],
            //     onBeforePageLoad: function () {
            //         $('.loading').show();
            //     },
            //     onAfterPageLoad: function () {
            //         $('.loading').hide();
            //     },
            //     items: ".notifs",
            // });
        }
    }
</script>

<style scoped>

</style>