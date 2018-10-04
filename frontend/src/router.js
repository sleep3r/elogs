import Vue from 'vue/dist/vue.esm.js'
import Router from 'vue-router'
import VueCookies from 'vue-cookies'

import BasePage from './components/BasePage.vue'
import Dashboard from './components/Dashboard.vue'
import JournalPage from './components/JournalPage.vue'
import LoginPage from './components/LoginPage.vue'
import MessagesPage from './components/MessagesPage.vue'
import SettingsPage from './components/SettingsPage.vue'
import ModesPage from './components/ModesPage.vue'
import AddJournal from './components/AddJournal.vue'

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
                    path: '/dashboard',
                    name: 'dashboard',
                    component: Dashboard
                },
                {
                    path: '/:plant/:journal/:shift_id',
                    name: 'defaultJournalPage',
                    component: JournalPage
                },
                {
                    path: '/messages',
                    name: 'messagesPage',
                    component: MessagesPage
                },
                {
                    path: '/addjournal',
                    name: 'addJournal',
                    component: AddJournal
                },
                {
                    path: '/settings',
                    name: 'settingsPage',
                    component: SettingsPage
                },
                {
                    path: '/modes',
                    name: 'modesPage',
                    component: ModesPage
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
