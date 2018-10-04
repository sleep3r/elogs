<template>
    <header class="header sticky">
        <div class="header__logo" @click.prevent="$router.push('/')"><i class="fab fa-font-awesome"></i><span>&nbsp;E-Logs</span>
        </div>
        <div class="header__title">
            <span class="journal_title" v-if="$route.name !== 'modesPage'">{{$store.getters['journalState/plantVerboseName']}}</span>
            <template v-if="$route.params.journal && $route.name !== 'modesPage'">
                <i v-if="!$store.getters['journalState/isSynchronized']" class="fa fa-circle-o-notch" id="async" aria-hidden="true" style="color:red"> Синхронизация...</i>
                <i v-if="$store.getters['journalState/isSynchronized']" class="fa fa-check" id="sync" aria-hidden="true" style="color:springgreen"> Синхронизировано</i>
            </template>
        </div>
        <div class="header__user">
            <i class="fas fa-envelope user-messages-badge" @click="onMsgClick"></i>
            <i class="fas fa-bell"></i>
            <span class="user-name" @click="onUsernameClick">{{$store.getters['userState/username']}}</span>
            <i class="fas fa-user-circle" style="margin-right: 0"></i>
            <div class="user-menu">
                <ul class="menu">
                    <li class="user-menu__item">
                        <a href="" @click.prevent="onSettingsClick">
                            <i class="fas fa-cogs"></i>
                            <span class="caption">Настройки</span>
                        </a>
                    </li>
                    <li class="user-menu__item">
                        <a href="" @click.prevent="onAddJournal">
                            <i class="fas fa-journal-whills"></i>
                            <span class="caption">Добавить журнал</span>
                        </a>
                    </li>
                    <li class="user-menu__item">
                        <a href="" @click.prevent="onModesClick">
                            <i class="fas fa-sliders-h"></i>
                            <span class="caption">Режимы</span>
                        </a>
                    </li>
                    <li class="user-menu__item">
                        <a href="" @click.prevent="onMessagesClick">
                            <i class="fa fa-envelope"></i>
                            <span class="caption">Список сообщений </span>
                        </a>
                    </li>
                    <li class="user-menu__item">
                        <a href="javascript:;" data-toggle="modal" data-target="#SchemeModal">
                            <i class="fa fa-book"></i>
                            <span class="caption">Схема цехов </span>
                        </a>
                    </li>
                    <li class="user-menu__item">
                        <a href="javascript:;" data-toggle="modal" data-target="#MessageToDevelopersModal">
                            <i class="fas fa-user-edit"></i><span
                                class="caption">Оставить отзыв разработчикам</span>
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
            <div id="messages-app"></div>
        </div>
    </header>
</template>

<script>
    export default {
        name: "TopNav",
        methods: {
            onLogout() {
                this.$store.dispatch('userState/logout')
                    .then(() => {
                        this.$router.push('/login')
                    })
            },
            onUsernameClick() {
                let element = document.querySelector('.header .user-menu');
                element.classList.toggle('visible');
            },
            onMsgClick() {
                let element = document.querySelector('.user-notifications');
                element.classList.toggle('display');
            },
            onSettingsClick() {
                this.$router.push('/settings')
            },
            onAddJournal() {
                this.$router.push('/addjournal');
                this.onUsernameClick();
            },
            onMessagesClick() {
                this.$router.push('/messages');
                this.onUsernameClick()
            },
            onModesClick() {
                this.$router.push('/modes');
                this.onUsernameClick()
            }
        }
    }
</script>

<style scoped>

</style>