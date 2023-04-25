<template lang="pug">
    div(class="fs6 api-calls")
        div
            div
                span REST API&nbsp;
                a(href="https://www.interactivebrokers.com/api/doc.html", target="_tab") documentation
            button(type="button", v-on:click="customEndpoint", v-if="showRestApi") Custom Endpoint
        div
            div Non-brokerage Calls (only LST required)
            button(type="button", v-on:click="apiGet('/one/user')", v-if="showRestApi") User
            button(type="button", v-on:click="apiGet('/ibcust/marketdata/subscriptions')", v-if="showRestApi") MD Subscriptions
            button(type="button", v-on:click="gstatBulletins", v-if="showRestApi") GSTAT Bulletins
            button(type="button", v-on:click="secdefConid", v-if="showRestApi") Secdef (conid)
            button(type="button", v-on:click="secdefTicker", v-if="showRestApi") Secdef (Stock Ticker)
            button(type="button", v-on:click="referrerid", v-if="showRestApi") Referrer ID
            button(type="button", v-on:click="getAuthorizedConsumers", v-if="showRestApi") Get Authorized Consumers
            button(type="button", v-on:click="revokeConsumer", v-if="showRestApi") Revoke Consumer (consumer)
        div
            div IServer Session
            button(type="button", v-on:click="authStatus", v-if="showRestApi") Auth Status
            button(type="button", v-on:click="ssoInit", v-if="showRestApi") Start Session
            button(type="button", v-on:click="iserverAccounts", v-if="showRestApi") Accounts
            button(type="button", v-on:click="searchSymbol", v-if="showRestApi") Search (Symbol)
            button(type="button", v-on:click="searchSymbolPost", v-if="showRestApi") Search POST (Symbol)
            button(type="button", v-on:click="searchName", v-if="showRestApi") Search (Name)
            button(type="button", v-on:click="marketdata", v-if="showRestApi") Market Data
            button(type="button", v-on:click="allMarketdata", v-if="showRestApi") All Market Data
            button(type="button", v-on:click="history", v-if="showRestApi") Historical MD
            button(type="button", v-on:click="orders", v-if="showRestApi") Live Orders
            button(type="button", v-on:click="getAlgos", v-if="showRestApi") IB Algos
            button(type="button", v-on:click="unsubAll", v-if="unsubAll") Unsubscribe All
            button(type="button", v-on:click="tickleSession", v-if="showRestApi") Tickle Session
            button(type="button", v-on:click="logout", v-if="showRestApi") Logout
        div
            div HMDS
            button(type="button", v-on:click="apiGet('/hmds/auth/init')", v-if="showRestApi") Init (Call this first)
            button(type="button", v-on:click="history(true)", v-if="showRestApi") History
            button(type="button", v-on:click="apiGet('/hmds/logout')", v-if="showRestApi") Logout
        div
            div MD
            button(type="button", v-on:click="apiGet('/md/auth/init')", v-if="showRestApi") Init (Call this first)
            button(type="button", v-on:click="snapshot(true)", v-if="showRestApi") Snapshot
            button(type="button", v-on:click="apiGet('/md/logout')", v-if="showRestApi") Logout
        div
            div Portfolio
            button(type="button", v-on:click="apiGet('/portfolio/accounts')", v-if="showRestApi") Accounts
            button(type="button", v-on:click="apiGet('/portfolio/subaccounts')", v-if="showRestApi") Subaccounts
        div
            div Portfolio2
            button(type="button", v-on:click="apiGet('/portfolio2/accounts')", v-if="showRestApi") Accounts
            button(type="button", v-on:click="apiGet('/portfolio2/subaccounts')", v-if="showRestApi") Subaccounts
        div
            div CCP Session (Beta) (ST required)
            small Note: IServer and CCP services can't be used at the same time.
            div
            button(type="button", v-on:click="apiGet('/ccp/status')", v-if="showRestApi") status
            button(type="button", v-on:click="ccpInit", v-if="showRestApi") init session
            button(type="button", v-on:click="apiGet('/ccp/accounts')", v-if="showRestApi") accounts
            button(type="button", v-on:click="queryCcpWithAcct('/ccp/positions')", v-if="showRestApi") positions
            button(type="button", v-on:click="queryCcpWithAcct('/ccp/orders')", v-if="showRestApi") orders
            button(type="button", v-on:click="queryCcpTrades('/ccp/trades')", v-if="showRestApi") trades
            button(type="button", v-on:click="logout", v-if="showRestApi") logout
        div(class="before-md", class="w100")
            h5(v-if="output.value.length > 0") Output
            pre(class="w100") {{ output.value }}
</template>

<script>
import mxGlobal from '../mixins/mx-global.js'
import mxOauth from '../mixins/mx-oauth.js'

export default {
    name: 'rest-api-view',
    mixins: [mxGlobal, mxOauth],
    data() {
        return {
            ccpAcct: ''
        }
    },
    methods: {
        referrerid: function() {
            const ep = '/one/referrerid';
            const acctId = prompt('Account ID');
            this.sendProtectedResourceRequest(this.getOptions(ep), 'POST', {acctId}, 'json').then(function (res) {
                this.handleApiResponse(res);
            }.bind(this));
        },
        allMarketdata: function () {
            this.apiGet('/iserver/marketdata');
        },
        getAuthorizedConsumers: function () {
            this.apiGet('/oauth/get_authorized_consumers');
        },
        gstatBulletins: function () {
            const ep = '/gstat/bulletins';
            var options = this.getOptions(ep);
            options.url = 'https://api.ibkr.com/v1/gstat/bulletins';
            this.sendProtectedResourceRequest(options, 'POST', { p: 'login', type: 'maintenance' }, 'json').then(function (res) {
                this.handleApiResponse(res);
            }.bind(this));
        },
        marketdata: function () {
            const conid = prompt('Conid', '8314');
            const fields = 'fields=30,55,70,72,82,83,84,85,6008,6004,6070';
            this.apiGet('/iserver/marketdata/snapshot?' + fields + '&conids=' + conid);
        },
        authStatus: function () {
            this.apiGet('/iserver/auth/status');
        },
        tickleSession: function () {
            this.apiGet('/tickle');
        },
        logout: function () {
            this.apiGet('/logout');
        },
        history: function (hmds) {
            const conid = prompt('Conid?', '8314');
            var mount = '/iserver/marketdata';
            if (hmds == true) {
                mount = '/hmds';
            }
            this.apiGet(mount + '/history?conid=' + conid + '&period=1w&bar=15min');
        },
        orders: function () {
            this.apiGet('/iserver/account/orders');
        },
        searchSymbol: function () {
            const symbol = prompt('Symbol', 'FB');
            this.apiGet('/iserver/secdef/search?symbol=' + symbol + '&name=false');
        },
        searchSymbolPost: function () {
            const symbol = prompt('Symbol', 'FB');
            const ep = '/iserver/secdef/search?symbol=' + symbol + '&name=false';
            this.sendProtectedResourceRequest(this.getOptions(ep), 'POST', {symbol: symbol}, 'json').then(function (res) {
                this.handleApiResponse(res);
            }.bind(this));
        },
        revokeConsumer: function () {
            const consumer = prompt('consumer', 'TESTCONS');
            const ep = '/oauth/deauthorize';
            this.sendProtectedResourceRequest(this.getOptions(ep), 'POST', {consumer: consumer}, 'json').then(function (res) {
                this.handleApiResponse(res);
            }.bind(this));
        },
        searchName: function () {
            const name = prompt('Company Name', 'FACEBOOK');
            this.apiGet('/iserver/secdef/search?symbol=' + name + '&name=true');
        },
        iserverAccounts: function () {
            this.apiGet('/iserver/accounts');
        },
        unsubAll: function () {
            this.apiGet('/iserver/marketdata/unsubscribeall');
        },
        getAlgos: function () {
            const conid = prompt('Conid:', '8314');
            const params = prompt('Parameters (e.g. adddescription=1&addParams=1):', '');
            var ep = '/iserver/contract/' + conid + '/algos';
            if (params.length > 0) {
                ep = ep + '?' + params;
            }
            this.apiGet(ep);
        },
        customEndpoint: function () {
            const ep = prompt('Please enter the endpoint you want to test:', '/one/user');
            const method = prompt('Please enter the request method type (e.g. GET, POST etc.):', 'GET');

            this.sendProtectedResourceRequest(this.getOptions(ep), method.toUpperCase(), {}).then(function (res) {
                this.handleApiResponse(res);
            }.bind(this));
        },
        getAcctParam: function() {
            return '?acct=' + this.acct

        },
        queryCcpTrades: function(endpoint) {
            const ep = prompt('Number of days back? 1-7', 1);
            if (!ep) {
                return;
            }
            this.ccpAcct = ep;
            this.apiGet(endpoint + '?from=' + ep * -1);
        },
        queryCcpWithAcct: function(endpoint) {
            const ep = prompt('Acct Number', this.ccpAcct);
            if (!ep) {
                return;
            }
            this.ccpAcct = ep;
            this.apiGet(endpoint + '?acct=' + ep);
        },
        ccpInit: function () {
            const compete = confirm('Compete with other sessions?');
            const locale = 'en_US';
            const options = this.getOptions('/ccp/auth/init');
            const body = {
                username: '-',
                machineId: this.settings.machineId,
                mac: this.settings.mac,
                compete,
                locale
            };
            console.log(body);
            this.oauthRequest(options, 'protectedResource', 'POST', body).then((res) => {
                console.log(res);
                this.handleApiResponse(res);
                if (res && res.authenticated) {
                    return;
                }
                console.log('challenge ST', this.credentials.ST, 'challenge', res.challenge);
                const R = window.compute_sk(res.challenge, this.credentials.ST);
                const options1 = this.getOptions('/ccp/auth/response');
                console.log('challenge response', R);
                this.handleApiResponse(res);
                this.oauthRequest(options1, 'protectedResource', 'POST', {response: R})
                    .then((res) => {
                        console.log(res);
                        this.handleApiResponse(res);
                    });
            });
        },
        ssoInit: function () {
            const compete = confirm('Compete with other sessions?');
            const locale = 'en_US';
            const tz = "xxx (America/New_York)";
            const options = this.getOptions('/iserver/auth/ssodh/init?publish=true&compete=' + compete);
            const body = {
                locale,
                tz
            };
            console.log(body);
            this.oauthRequest(options, 'protectedResource', 'POST', body, 'json').then((res) => {
                this.handleApiResponse(res);
            });
        },
        secdefConid: function () {
            const conid = prompt('Conid', '8314');
            this.apiGet('/trsrv/secdef?conids=' + conid);
        },
        secdefTicker: function () {
            const conid = prompt('Symbols', 'IBKR,MSFT,AAPL');
            this.apiGet('/trsrv/stocks?symbols=' + conid);
        },
        snapshot: function (md) {
            const conid = prompt('Conids', '8314');
            var mount = '/iserver/marketdata';
            if (md == true) {
                mount = '/md';
            }
            this.apiGet(mount + '/snapshot?conids=' + conid + 'fields=6509,86,84,75,31,83,72,7891,7292,74,78,55,7219');
        }
    }
}
</script>

<style>
.api-calls > div {
    margin: 1em 0;
}
</style>