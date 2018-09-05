import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import EditPage from './views/EditPage.vue'
import CreateTablePage from './views/CreateTablePage.vue'
import CreateJournalPage from './views/CreateJournalPage.vue'
import JournalPage from './views/Journal.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/journal/:journalName/table/:tableName/edit',
      name: 'edit',
      component: EditPage
    },
    {
      path: '/journal/create',
      name: 'createJournal',
      component: CreateJournalPage
    },
    {
      path: '/journal/:name/table/create',
      name: 'createTable',
      component: CreateTablePage
    },
    {
      path: '/journal/:name',
      name: 'journal',
      component: JournalPage
    }
  ]
})
