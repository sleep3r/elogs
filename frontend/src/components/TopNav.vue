<template>
    <header class="header sticky">
        <div class="header__logo" @click.prevent="$router.push('/')"><b>E-LOGS</b></div>
        <div class="header__title">
            <!--<span class="plant_title" v-if="$route.name === 'defaultJournalPage'">{{$store.getters['journalState/plantVerboseName']}}</span>-->
            <!--<template v-if="$route.params.journal && $route.name !== 'modesPage'">-->
                <!--<i v-if="!$store.getters['journalState/isSynchronized']" class="fa fa-circle-o-notch" id="async" aria-hidden="true" style="color: #ca0000"> Синхронизация...</i>-->
                <!--<i v-if="$store.getters['journalState/isSynchronized']" class="fa fa-check" id="sync" aria-hidden="true" style="color: #36d686"> Синхронизировано</i>-->
            <!--</template>-->
        </div>
        <div class="header__user">
            <i class="fas fa-envelope user-messages-badge" @click="onMessagesClick"></i>
            <i class="fas fa-bell user-notify" @click="onNotifyClick">
                <div class="notify-badge">{{getUnreadedMessages.length < 100 ? getUnreadedMessages.length : '*'}}</div>
            </i>
            <div class="notify-menu-wrapper">
                <div class="notify-menu">
                    <template v-if="getUnreadedMessages.length">
                        <div class="msg-container">
                            <ul class="menu">
                                <li class="user-menu__item message" v-for="message in getUnreadedMessages" :key="message.id">
                                    <a href="" @click.prevent="onMessagesClick">
                                        <div v-if="message.sendee" class="message__title__container">
                                            <!-- <span class="message__author-name">{{ message.user_name }}</span> -->
                                            <strong class="message__title">
                                                <span class="sendee">{{message.sendee}}</span>
                                            </strong>
                                            <strong class="message__title">
                                                <span class="message__info">{{message.type}}</span>
                                            </strong>
                                        </div>
                                        <template>
                                            <p :class="['message__text', message.type]">{{message.text}}</p>
                                            <span class="message__created">{{new Date(message.created).toLocaleString()}}</span>
                                        </template>
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </template>
                    <template v-else>
                        <div class="no-msg-container">
                            <span>Сообщений нет</span>
                        </div>
                    </template>
                </div>
            </div>
            <i class="fas fa-home default-page-badge" @click="makeDefaultPage"></i>
            <span class="user-name" @click="onUsernameClick">{{$store.getters['userState/fullname']}}</span>
            <i class="fas fa-user-circle" style="margin-right: 0"></i>
            <div class="user-menu-wrapper">
                <div class="user-menu">
                    <ul class="menu">
                        <li class="user-menu__item">
                            <!--<a href="" @click.prevent="onSettingsClick">-->
                                <!--<i class="fas fa-cogs"></i>-->
                                <!--<span class="caption">Настройки</span>-->
                            <!--</a>-->
                        </li>
                        <li class="user-menu__item">
                            <a href="" @click.prevent="onAddJournal">
                                <i class="fas fa-journal-whills"></i>
                                <span class="caption">Добавить журнал</span>
                            </a>
                        </li>
                        <li class="user-menu__item" v-if="$store.getters['userState/isSuperuser'] || $store.getters['userState/hasPerm']">
                            <a href="" @click.prevent="onOpenConstructor">
                                <i class="fas fa-atom"></i>
                                <span class="caption">Открыть конструктор</span>
                            </a>
                        </li>
                        <li class="user-menu__item" v-if="$store.getters['userState/hasPerm']('validate_cells') || $store.getters['userState/isSuperuser']">
                            <a href="" @click.prevent="onModesClick">
                                <i class="fas fa-sliders-h"></i>
                                <span class="caption">Режимы</span>
                            </a>
                        </li>
                        <li class="user-menu__item">
                            <a href="javascript:;" data-toggle="modal" data-target="#SchemeModal" @click="hideUserMenu">
                                <i class="fa fa-book"></i>
                                <span class="caption">Схема цехов </span>
                            </a>
                        </li>
                        <li class="user-menu__item">
                            <a href="" @click.prevent="onLogout">
                                <i class="fas fa-sign-out-alt"></i>
                                <span class="caption">Выйти из системы</span>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
            <div id="messages-app"></div>
        </div>
    </header>
</template>

<script>
    import ajax from '../axios.config'
    export default {
        name: "TopNav",
        computed: {
            getUnreadedMessages () {
                return this.$store.getters['messagesState/unreadedMessages']
            }
        },
        methods: {
            onLogout() {
                this.$store.dispatch('userState/logout')
                    .then(() => {
                        this.$router.push('/login')
                    })
            },
            onNotifyClick() {
                if ($('.header .notify-menu').hasClass('menu-visible')) {
                    this.hideNotifyMenu()
                }
                else {
                    this.showNotifyMenu()
                }
            },
            onOpenConstructor () {
                window.open(`http://${window.location.hostname === 'localhost' ?
                    '127.0.0.1'
                    : window.location.hostname}:8085`,
                '_blank')
            },
            showNotifyMenu () {
                $('.header .notify-menu').addClass('menu-visible')
                $('.header .notify-menu-wrapper').addClass('menu-visible')
            },
            hideNotifyMenu () {
                $('.header .notify-menu').removeClass('menu-visible')
                $('.header .notify-menu-wrapper').removeClass('menu-visible')
            },
            onUsernameClick() {
                if ($('.header .user-menu').hasClass('menu-visible')) {
                    this.hideUserMenu()
                }
                else {
                    this.showUserMenu()
                }
            },
            showUserMenu () {
                $('.header .user-menu').addClass('menu-visible')
                $('.header .user-menu-wrapper').addClass('menu-visible')
            },
            hideUserMenu () {
                $('.header .user-menu').removeClass('menu-visible')
                $('.header .user-menu-wrapper').removeClass('menu-visible')
            },
            onMsgClick() {
                let element = document.querySelector('.user-notifications');
                element.classList.toggle('display');
            },
            onSettingsClick() {
                this.$router.push('/settings')
                // this.hideUserMenu();
            },
            onAddJournal() {
                this.$router.push('/addjournal');
                // this.hideUserMenu();
            },
            onMessagesClick() {
                this.$router.push('/messages');
                // this.hideUserMenu()
            },
            onModesClick() {
                this.$router.push('/modes');
                this.hideUserMenu()
            },
            makeDefaultPage(event) {
                var path = window.location.pathname
                console.log(event.target)
                // event.target.classList.remove("fa-home")
                // event.target.classList.add("fa-check-circle")
                ajax.post(
                    "http://localhost:8000/api/setting/",
                    {
                        "name": "defaultpage",
                        "value": path,
                    }
                )
            },
        },
        mounted () {
            let _this = this

            this.$store.dispatch('messagesState/loadUnreadedMessages')
                .then(() => {
                    if (this.getUnreadedMessages.length) {
                        this.$notify({
                            title: 'Новые сообщения',
                            text: `У вас ${this.getUnreadedMessages.length} новых сообщений!`,
                            duration: 5000
                        })
                    }
                })

            $('.header .user-menu-wrapper').click(function () {
                _this.hideUserMenu()
            })
            $('.header .notify-menu-wrapper').click(function () {
                _this.hideNotifyMenu()
            })
        }
    }
</script>

<style scoped>

</style>
