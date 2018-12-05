import Vue from 'vue/dist/vue.esm.js'
import Router from 'vue-router'
import VueCookies from 'vue-cookies'
import EventBus from './EventBus'

import BasePage from './components/BasePage.vue'
import Dashboard from './components/Dashboard.vue'
import JournalPage from './components/JournalPage.vue'
import LoginPage from './components/LoginPage.vue'
import MessagesPage from './components/MessagesPage.vue'
import SettingsPage from './components/settings-page/SettingsPage.vue'
import ModesPage from './components/ModesPage.vue'
import AddJournal from './components/AddJournal.vue'
import ajax from './axios.config.js'
import store from './store/store.js'


Vue.use(Router);

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
    if (!VueCookies.get('Authorization') && to.path !== '/login') {
        $('.modal-backdrop').css({'display': 'none'})
        next('/login')
    }
    else {
        console.dir(VueCookies.get('Authorization'))
        console.log(to)
        if (to.path == "/") {
            let defaultPage = store.getters['userState/defaultPage']
            console.log('dp', defaultPage)
            if (defaultPage) {
                var location = defaultPage.split("/")
                console.log('location', location)

                if (location.length > 2) {
                    var payload = {
                        "plantName": location[1],
                        "journalName": location[2],
                    }
                    EventBus.$emit("set-menu-journal-item", payload)
                }
                else if (location[1] == "dashboard") {
                    EventBus.$emit("set-menu-dashboard-item")
                }
                next(defaultPage)
            }
            else {
                next("/dashboard")
            }
        }
        else {
            next()
        }
    }
})

export default router
