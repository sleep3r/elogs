import Vue from 'vue/dist/vue.esm.js'
import Router from 'vue-router'
import VueCookies from 'vue-cookies'

import BasePage from './components/BasePage.vue'
import JournalPage from './components/JournalPage.vue'
import LoginPage from './components/LoginPage.vue'
import MessagesPage from './components/MessagesPage.vue'
import SettingsPage from './components/SettingsPage.vue'

Vue.use(Router)

const router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'basePage',
            component: BasePage,
            children: [
                {
                    path: '/:plant/:journal/:shift_id',
                    name: 'journalPage',
                    component: JournalPage
                },
                {
                    path: '/messages',
                    name: 'messagesPage',
                    component: MessagesPage
                },
                {
                    path: '/settings',
                    name: 'settingsPage',
                    component: SettingsPage
                }
            ]
        },
        {
            path: '/login',
            name: 'loginPage',
            component: LoginPage
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (!VueCookies.get('Authorization') && to.name !== 'loginPage') {
        next('/login')
    }
    else {
        next()
    }
})

export default router
