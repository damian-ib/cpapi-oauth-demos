import VueRouter from 'vue-router'

import orderTicketView from './order-ticket.vue'
import portfolioView from './portfolio-view.vue'
import restApiView from './rest-api-view.vue'
import streamingApiView from './streaming-api-view.vue'
import landingPageView from './landing.vue'
import legacyApiView from './legacy-api-view.vue'

const routes = [
    {path: '/orderticket', component: orderTicketView},
    {path: '/portfolio', component: portfolioView},
    {path: '/orderticket', component: orderTicketView},
    {path: '/restapi', component: restApiView},
    {path: '/streamingapi', component: streamingApiView},
    {path: '/legacyapi', component: legacyApiView},
    {path: '*', component: landingPageView}
]

const router = new VueRouter({
    routes
})

export default router;