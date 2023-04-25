<template lang="pug">
    div(class="fs6 api-calls legacy-settings")
        div
            span Legacy REST API&nbsp;
            a(href="https://www.interactivebrokers.com/webtradingapi/doc.html", target="_tab") documentation
        div
            span Paper:
            a(href="", @click.prevent="isPaper = !isPaper") {{ isPaper ? 'On' : 'Off' }}
        div
            table
                tr
                    td Legacy API Base URL:
                    td
                        input(v-model="legacyBaseUrl")
        div
            button(type="button", v-on:click="secdefConid", v-if="showRestApi") Secdef (conid)
            button(type="button", v-on:click="accounts", v-if="showRestApi") Accounts
            button(type="button", v-on:click="positions", v-if="showRestApi") Positions
            button(type="button", v-on:click="summary", v-if="showRestApi") Summary
            button(type="button", v-on:click="orders", v-if="showRestApi") Orders
            button(type="button", v-on:click="trades", v-if="showRestApi") Trades
            button(type="button", v-on:click="snapshot", v-if="showRestApi") Marketdata Snapshot (conid)
        div(class="before-md", class="w100")
            h5(v-if="output.value.length > 0") Output
            pre(class="w100") {{ output.value }}
</template>

<script>
    import mxGlobal from '../mixins/mx-global.js'
    import mxOauth from '../mixins/mx-oauth.js'

    export default {
        name: 'legacy-api-view',
        mixins: [mxGlobal, mxOauth],
        data() {
            return {
                isPaper: false,
                legacyBaseUrl: 'https://www.interactivebrokers.com',
                accountId: ''
            }
        },
        computed: {
            baseUrl() {
                return this.legacyBaseUrl + (this.isPaper ? '/ptradingapi/v1' : '/tradingapi/v1');
            }
        },
        methods: {
            accounts: function () {
                this.apiGet('/accounts', this.baseUrl);
            },
            positions: function() {
                const account = prompt('Account ID', this.accountId);
                this.accountId = account;
                this.apiGet('/accounts/' + account + '/positions', this.baseUrl);
            },
            summary: function() {
                const account = prompt('Account ID', this.accountId);
                this.accountId = account;
                this.apiGet('/accounts/' + account + '/summary', this.baseUrl);
            },
            orders: function() {
                const account = prompt('Account ID', this.accountId);
                this.accountId = account;
                this.apiGet('/accounts/' + account + '/orders', this.baseUrl);
            },
            trades: function() {
                const account = prompt('Account ID', this.accountId);
                this.accountId = account;
                this.apiGet('/accounts/' + account + '/trades', this.baseUrl);
            },
            secdefConid: function () {
                const conid = prompt('Conid', '8314');
                this.apiGet('/secdef?conid=' + conid, this.baseUrl);
            },
            snapshot: function () {
                const conid = prompt('Conids', '8314');
                this.apiGet('/marketdata/snapshot?conids=' + conid, this.baseUrl);
            }
        }
    }
</script>

<style lang="less">
    .legacy-settings table {
        width: 100%;

        tr {
            vertical-align: top;
        }

        td:last-child {
            width: 70%;
            > input {
                width: 80%;
            }
            > button {
                width: 20%;
            }
        }

        each(range(4), {
            .col-@{value} {
                height: (@value * 50px);
            }
        });
    }
    .api-calls > div {
        margin: 1em 0;
    }
</style>