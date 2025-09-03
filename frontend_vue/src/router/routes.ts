import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', component: () => import('@/views/CategoriesView.vue'),
    },
    {
      path: '/list-videos/:category', component: () => import('@/views/PlayVideoList.vue'),
    },
    {
      path: '/remote', component: () => import('@/views/RemoteView.vue'),
    },
    {
      path: '/admin', component: () => import('@/views/AdminView.vue'),
      children: [
        {path: 'library', component: ()  => import('@/views/AdminViewLibrary.vue')},
        {path: 'db', component: ()  => import('@/views/AdminViewLocalDB.vue')},
        {path: 'kinopoisk', component: ()  => import('@/views/AdminViewKinopoisk.vue')},
        {path: 'backups', component: ()  => import('@/views/AdminViewBackup.vue')}
      ]
    },
    {
      path: '/iptv', component: () => import('@/views/IPTVView.vue'),
    }
  ],
})

export default router
