import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './assets/base.css';

import App from './App.vue'
import router from './router/routes.ts'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
