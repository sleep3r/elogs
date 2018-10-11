import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import EditPage from './views/EditTableDataPage.vue'
import CreateTablePage from './views/CreateTablePage.vue'
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
      path: '/journal/:journalName/table/:tableName/edit_data',
      name: 'editData',
      component: EditPage
    },
    {
      path: '/journal/:journalName/table/create',
      name: 'createTable',
      component: CreateTablePage
    },
    {
      path: '/journal/:journalName',
      name: 'journal',
      component: JournalPage
    }
  ]
})
