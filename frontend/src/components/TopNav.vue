<template>
    <header class="header sticky">
        <div class="header__logo" @click.prevent="$router.push('/')" data-toggle="tooltip" title="Вернуться на домашнюю страницу"><b>E-LOGS</b></div>
        <div class="header__title">
            <div class="offline-warn" v-if="isOffline">Внимание, вы работаете в оффлайн режиме!</div>
        </div>
        <div class="header__user">
            <div @click="onNotifyClick" class="user-notify-container" data-toggle="tooltip" title="Сообщения">
                <i class="fas fa-bell user-notify">
                <div v-if="getUnreadedMessages > 0" class="notify-badge">{{getUnreadedMessages.length < 100 ? getUnreadedMessages.length : '*'}}</div>
            </i>
            </div>
            <div class="notify-menu-wrapper">
                <div class="notify-menu">
                    <template v-if="getUnreadedMessages.length">
                        <div class="msg-container">
                            <ul class="menu">
                                <li class="user-menu__item message" v-for="message in getUnreadedMessages" :key="message.id">
                                    <a href="" @click.prevent="onMessagesClick">
                                        <div v-if="message.sendee" class="message__title__container">
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
                            <div style="margin-bottom: 8px;">Новых сообщений нет</div>
                            <ul class="menu">
                                <li class="user-menu__item" v-if="$store.getters['userState/isSuperuser'] || $store.getters['userState/hasPerm']">
                                    <a href=""  @click.prevent="onMessagesClick">
                                        <i class="fas fa-envelope user-messages-badge"></i>
                                        <span class="caption">Все сообщения</span>
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </template>
                </div>
            </div>
            <i class="fas fa-home default-page-badge" :class="{'is-home': isCurrentPage }" @click="onHomeClick" data-toggle="tooltip" title="Домашняя страница"></i>
            <span class="user-name" @click="onUsernameClick" data-toggle="tooltip" title="Профиль пользователя">{{$store.getters['userState/fullname']}}</span>
            <div class="user-menu-wrapper">
                <div class="user-menu">
                    <ul class="menu">
                        <li class="user-menu__item" v-if="$store.getters['userState/isSuperuser'] || $store.getters['userState/hasPerm']">
                            <a href="" @click.prevent="onAddJournal">
                                <i class="fas fa-journal-whills"></i>
                                <span class="caption">Добавить журнал</span>
                            </a>
                        </li>
                        <li class="user-menu__item">
                            <a href="javascript:;" data-toggle="modal" data-target="#SchemeModal" @click="hideUserMenu">
                                <i class="fa fa-book"></i>
                                <span class="caption">Схема цехов </span>
                            </a>
                        </li>
                        <li class="user-menu__item" v-if="!$store.getters['userState/isBoss'] || $store.getters['userState/isSuperuser']">
                            <a href="javascript:;" data-toggle="modal" data-target="#NoBossInstruction" @click="hideUserMenu">
                                <i class="fa fa-book"></i>
                                <span class="caption">Инструкция </span>
                            </a>
                        </li>
                        <li class="user-menu__item" v-if="$store.getters['userState/isBoss'] || $store.getters['userState/isSuperuser']">
                            <a href="javascript:;" data-toggle="modal" data-target="#BossInstruction" @click="hideUserMenu">
                                <i class="fa fa-book"></i>
                                <span class="caption">Инструкция для руководства </span>
                            </a>
                        </li>
                        <li class="user-menu__item">
                            <a href="" @click.prevent="onPrint">
                                <i class="fas fa-print"></i>
                                <span class="caption">Печать</span>
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
    import EventBus from '../EventBus'
import { setTimeout } from 'timers';

    export default {
        name: "TopNav",
        data () {
            return {
                onlineTimer: null,
                isOffline: false,
                isCurrentPage: this.$route.path === this.$store.getters['userState/defaultPage']
            }
        },
        watch: {
            $route (value) {
                this.setIsCurrentPage()
            }
        },
        computed: {
            getUnreadedMessages () {
                return this.$store.getters['messagesState/unreadedMessages']
            }
        },
        methods: {
            setIsCurrentPage () {
                this.isCurrentPage = this.$route.path === this.$store.getters['userState/defaultPage']
            },
            startCheckingOffline () {
                this.onlineTimer = setInterval(() => {
                    if (window.navigator.onLine) {
                        this.isOffline = false
                    }
                    else {
                        this.isOffline = true
                    }
                }, 1000)
            },
            stopCheckingOffline () {
                clearInterval(this.onlineTimer)
                this.onlineTimer = null
            },
            onPrint () {
                this.$store.commit('journalState/SET_FOR_PRINT', true)
                setTimeout(() => {
                    window.print()
                    this.$store.commit('journalState/SET_FOR_PRINT', false)
                }, 0)

            },
            onLogout() {
                this.$store.dispatch('userState/logout')
                    .then(() => {
                        this.$disconnect()
                    })
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
                window.open(`${window.location.hostname === 'localhost' ?
                    'http://127.0.0.1:8085'
                    : window.FRONT_CONSTRUCTOR_HOSTNAME}`,
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
            onHomeClick() {
                if (!this.isCurrentPage) {
                    EventBus.$emit('open-alert', {
                        onOk: this.makeDefaultPage,
                        text: 'Текущая страница будет вашей домашней'
                    })
                }
                else if (this.$route.name !== 'dashboard') {
                    EventBus.$emit('open-alert', {
                        onOk: this.restoreDefaultPage,
                        text: 'Домашняя страница будет сброшена'
                    })
                }
            },
            makeDefaultPage(event) {
                let path = window.location.pathname;
                console.log("path", path);
                this.$store.dispatch('userState/setDefaultPage', {
                    path: path,
                })
                    .then(resp => {
                        this.$store.dispatch('userState/getDefaultPage')
                        .then(() => {
                            this.setIsCurrentPage()
                        })
                    })
            },
            restoreDefaultPage(event) {
                let path = window.location.pathname

                this.$store.dispatch('userState/setDefaultPage', {
                    path: '/dashboard',
                })
                    .then(resp => {
                        this.$store.dispatch('userState/getDefaultPage')
                            .then(() => {
                                this.setIsCurrentPage()
                            })
                    })
            },
        },
        mounted () {
            console.info("route->", this.$route.path, " from get->", this.$store.getters['userState/defaultPage']);

            let _this = this

            this.startCheckingOffline()

            $('[data-toggle="tooltip"]').tooltip({delay: {show: 200, hide: 0}})

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
        },
        beforeDestroy () {
            this.stopCheckingOffline()
        }
    }
</script>

<style scoped lang="scss">
    .header__user {
        .is-home {
            color: yellow;
        }
    }
</style>
