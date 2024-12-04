import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/components/MainPageInfo.vue';
import About from '@/components/About.vue';
import Page1 from "@/components/Page1.vue";
import Page2 from "@/components/Page2.vue";

const routes = [
    { path: '/', component: Home },
    { path: '/about', component: About },
    { path: '/page1', component: Page1 },
    { path: '/page2', component: Page2 }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;