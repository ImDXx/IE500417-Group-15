import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router';
import './assets/main.css'; // Ensure this path is correct

const app = createApp(App);

app.use(router);

app.mount('#app');