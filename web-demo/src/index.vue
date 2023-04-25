<template lang="pug">
div(class="_con")
    div
        a(href="#" v-on:click="toggleUsage") How to use
        span &nbsp;|&nbsp;
        a(href="#" v-on:click="toggleOAuthSettings") OAuth Settings
        span &nbsp;|&nbsp;
        a(href="https://api.ibkr.com/v1/api/internal/changelog" target="_blank") Prod Changelog
        span &nbsp;|&nbsp;
        a(href="https://api.ibkr.com/alpha/api/internal/changelog" target="_blank") Alpha Changelog
        span(class="dev-mode")
            | Dev Mode:
            a(href="", @click.prevent="session.isDev = !session.isDev") {{ session.isDev ? 'On' : 'Off' }}
            span &nbsp;
            | Env:
            a(href="", @click.prevent="switchEnv") {{ sessionEnv }}
            span &nbsp;
            | GW:
            a(href="", @click.prevent="session.useGw = !session.useGw") {{ session.useGw ? 'On' : 'Off' }}
    ib-usage(v-if="showUsage")
    ib-oauth-settings(v-if="showOAuthSettings")
    div(class="fs5 before-lg after-lg")
        b Test Components:
        ul(class="component-menu")
            li
                router-link(to="orderticket") Order Ticket
            li
                router-link(to="portfolio") Portfolio
            li
                router-link(to="restapi") REST API
            li
                router-link(to="streamingapi") Streaming API
            li
                router-link(to="legacyapi") Legacy API
    keep-alive
        router-view(class="before-lg")
</template>

<script>

import mxGlobal from './mixins/mx-global.js'
import mxOauth from './mixins/mx-oauth.js'

export default {
    mixins: [ mxGlobal, mxOauth ],
	data: {
        showUsage: false,
        showOAuthSettings: true,
		orders: []
	},
    computed: {
        sessionEnv() {
            return this.session.baseUrl.includes('/alpha') ? 'Alpha' : 'Prod';
        }
    },
	methods: {
        switchEnv() {
            const isAlpha = this.sessionEnv.toLowerCase() == 'alpha';
            if (isAlpha) {
                this.session.baseUrl = this.session.baseUrl.replace('/alpha', '/v1');
            } else {
                this.session.baseUrl = this.session.baseUrl.replace('/v1', '/alpha');
            }
            console.debug('baseUrl switched to', this.session.baseUrl);
        },
        toggleUsage() {
            this.showUsage = !this.showUsage;
        },
        toggleOAuthSettings() {
            this.showOAuthSettings = !this.showOAuthSettings;
        }
	}
}
</script>

<style>
    .component-menu {
        padding: 0;
        margin: 0 10px;
        display: inline;
    }
    .dev-mode {
        float: right;
    }
    .component-menu li {
        list-style: none;
        display: inline;
        padding-right: 10px;
    }
</style>