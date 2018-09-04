import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import EditPage from './views/EditPage.vue'
import CreatePage from './views/CreatePage.vue'

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
      path: '/edit/:name',
      name: 'edit',
      component: EditPage
    },
    {
      path: '/create',
      name: 'create',
      component: CreatePage
    }
  ]
})
