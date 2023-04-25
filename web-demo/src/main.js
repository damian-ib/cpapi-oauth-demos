import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './index.vue'

import store from './js/store';
import router from './views/router'

import ibKeySettings from './ib/ib-key-settings.vue';
import ibUsage from './ib/ib-usage.vue'
import ibOAuthSettings from './ib/ib-oauth-settings.vue'
import positions from './components/positions.vue'
import orders from './components/orders.vue'

require('./styles/global.less');

Vue.use(VueRouter);

Vue.component('key-settings', ibKeySettings);
Vue.component('ib-oauth-settings', ibOAuthSettings);
Vue.component('ib-usage', ibUsage);

Vue.component('positions', positions);
Vue.component('orders', orders);

const fetch = require('node-fetch')
global.Headers = fetch.Headers;

const app = new Vue({
    store,
    router,
	...App
});

app.$mount('#app');
window.app = app;
