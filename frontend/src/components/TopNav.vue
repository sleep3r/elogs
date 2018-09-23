<template>
    <header class="header sticky">
        <div class="header__logo"> <i class="fab fa-font-awesome"></i><span>&nbsp;E-Logs</span></div>
        <div class="header__title">
            <span class="journal_title">{{$store.getters['journalState/plantName']}}</span>
             <!--if plant-->
            <!--<i class="fa fa-circle-o-notch" id="async" aria-hidden="true" style="display:none; color:red"> Синхронизация...</i>-->
            <!--<i class="fa fa-check" id="sync" aria-hidden="true" style="display:none; color:springgreen"> Синхронизировано</i>-->
            <!---->
        </div>
        <div class="header__user">
            <i class="fas fa-envelope user-messages-badge" onclick="Toggle.class('.user-notifications','display')"></i>
            <i class="fas fa-bell"></i>
            <span class="user-name">?? user.employee ??</span>
            <i class="fas fa-user-circle"></i>
            <div class="user-menu">
                <ul class="menu">
                    <li class="user-menu__item">
                        <a href="/common/settings/">
                            <i class="fas fa-cogs"></i>
                            <span class="caption">Настройки</span>
                        </a>
                    </li>
                    <li class="user-menu__item">
                        <a href="/common/messages/list/">
                            <i class="fa fa-envelope" ></i>
                            <span class="caption">Список сообщений </span>
                        </a>
                    </li>
                    <li class="user-menu__item">
                        <a href="javascript:;" data-toggle="modal" data-target="#SchemeModal">
                            <i class="fa fa-book" ></i>
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
                        <a href="/auth/logout">
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
    name: "TopNav"
}
</script>

<style scoped>

</style>