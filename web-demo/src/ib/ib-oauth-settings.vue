<template lang="pug">
    div(class="before-lg oauth-settings")
        div(class="store-settings text-right")
            a(href="", @click.prevent="storeState") Store State
            a(href="", @click.prevent="restoreState") Restore State
            a(href="", @click.prevent="clearState") Clear Store
        table(v-if="session.useGw")
            tr
                td Gateway Base URL
                td
                    input(v-model="session.gwBaseUrl")
        table(v-else)
            tr(v-if="session.isDev")
                td Base URL
                td
                    input(v-model="session.baseUrl")
            tr
                td Consumer Key
                td
                    input(v-model="credentials.consKey")
                    key-settings
            tr
                td Realm
                td
                    input(v-model="credentials.realm")
            tr
                td Request Token (1. Step)
                td
                    input(v-model="oauth.requestToken")
                    button(type="button", v-on:click="requestTokenRequest") GET
            tr
                td Authorize IB User (2. Step)
                td
                    div
                        div(v-if="!oauth.requestToken") {{ authorizeUrl }}
                        div(v-else)
                            a(:href="authorizeUrl", target="_tab") Authorize User (WWW)
                            span  |&nbsp;
                            a(:href="authorizeUrl.replace('www', 'cdcdyn')", target="_tab") CHI (DR Link)
                            span  |&nbsp;
                            a(:href="authorizeUrl.replace('www', 'ndcdyn')", target="_tab") NY5 (Prod Link)
                        div
                            u Note
                            span  The request token can only be used once after user uses it to authorize access.
            tr
                td Verifier Token
                td
                    input(v-model="oauth.verifier")
            tr
                td Access Token (3. Step)
                td
                    input(v-model="credentials.accessToken")
                    button(type="button", v-on:click="accessTokenRequest") GET
            tr
                td Access Token Secret
                td
                    input(v-model="oauth.tokenSecret")
            tr
                td Live Session Token (4. Step)
                td
                    input(v-model="credentials.liveSessionToken")
                    button(type="button", v-on:click="liveSessionTokenRequest") GET
            tr(v-show="session.isDev")
                td LST BigInt
                td
                    span {{ credentials.lstBigInt && credentials.lstBigInt.toString(16) }}
</template>

<script>

    const NodeRSA = require('node-rsa')
    const crypto = require('crypto')
    const bigInteger = require('big-integer')

    import {
        calculateLST,
        verifyLST
    } from '../oauth.functions'

    import mxGlobal from '../mixins/mx-global.js'
    import mxOauth from '../mixins/mx-oauth.js'

    export default {
        name: 'ib-oauth-settings',
        mixins: [mxGlobal, mxOauth],
        data() {
            return {
                authorizeUrl: 'Click on GET request token to generate the authorize URL'
            }
        },
        created() {
            this.newMachineId();
        },
        watch: {
            ['oauth.requestToken'](prev, next) {
                this.authorizeUrl = 'https://www.interactivebrokers.com/authorize?oauth_token=' + prev
                 + '&redirect_uri=http:\\/\\/localhost:20000/';
            }
        },
        methods: {
            clearState() {
                localStorage.clear();
                alert('cleared');
                location.reload();
            },
            restoreState() {
                const store = JSON.parse(localStorage.getItem('oauth.state'));
                this.$set(this.$store.state, 'oauth', store.oauth);
                this.$set(this.$store.state, 'credentials', store.credentials);
                this.$set(this.$store.state, 'settings', store.settings);
                this.$set(this.$store.state, 'keys', store.keys);
                this.$set(this.$store.state, 'session', store.session);
            },
            storeState() {
                const store = {
                    'oauth': this.oauth,
                    'credentials': this.credentials,
                    'settings': this.settings,
                    'keys': this.keys,
                    'session': this.session
                }
                localStorage.setItem("oauth.state", JSON.stringify(store));
                alert('stored');
            },
            liveSessionTokenRequest: function () {
                var dhRandom = crypto.randomBytes(25).toString('hex');
                const A = bigInteger(this.keys.generator).modPow(bigInteger(dhRandom, 16), bigInteger(this.keys.prime, 16));
                console.log('a: ' + dhRandom.toString());
                console.log('A: ' + A.toString());
                const options = this.getOptions('/oauth/live_session_token');
                var deviceId = this.deviceId
                console.debug('credentials', this.credentials);
                options.accessToken = this.credentials.accessToken;
                options.diffieHellmanChallenge = A.toString(16)
                console.log(options.diffieHellmanChallenge);
                const key = new NodeRSA(this.keys.privateEncryptionKey);
                key.setOptions({
                    encryptionScheme: 'pkcs1'
                });
                var prepend = key.decrypt(this.oauth.tokenSecret, 'hex');
                options.prepend = prepend;
                console.log("secret: " + prepend);
                this.oauthRequest(options, 'liveSessionToken', 'POST', {device_id: deviceId}).then(function (res) {
                    if (res.diffie_hellman_response == "") {
                        alert("Please retry live session token generation!");
                        return;
                    }
                    let lst = calculateLST(res.diffie_hellman_response, dhRandom, Buffer.from(prepend, 'hex'), this.keys.prime);
                    this.credentials.liveSessionToken = lst;
                    this.credentials.lstBigInt = bigInteger(Buffer.from(lst, 'base64').toString('hex'), 16);
                    console.log('lst', lst);
                    console.log('verify lst', verifyLST(lst, options.consKey, res.live_session_token_signature));
                }.bind(this));
            },
            requestTokenRequest: function () {
                const options = this.getOptions('/oauth/request_token');
                this.oauthRequest(options, 'requestToken', 'POST', {}).then(function (res) {
                    this.oauth.requestToken = res.oauth_token;
                }.bind(this)).catch(function (err) {
                    console.log(err);
                });
            },
            accessTokenRequest: function () {
                var options = this.getOptions('/oauth/access_token');
                options.requestToken = this.oauth.requestToken;
                options.verifier = this.oauth.verifier;
                console.log(options.verifier);
                this.oauthRequest(options, 'accessToken', 'POST', {}).then(function (res) {
                    this.credentials.accessToken = res.oauth_token;
                    this.oauth.tokenSecret = res.oauth_token_secret;
                }.bind(this));
            },
        }
    }

</script>

<style lang="less">
    .oauth-settings table {
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
    .store-settings a {
        margin: 0 0.5em
    }

</style>
