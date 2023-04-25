<template lang="pug">
    div
        div(class="fs5 after-md") Streaming API
            span &nbsp;
            a(href="", @click.prevent="toggleWs") websocket {{ connected ? 'off' : 'on' }}
            div base url: {{ wsBaseUrl }}
        label subscriptions
        div
            button(@click="sendSession") send session (if waiting for session)
            button(@click="customWsRequest") send custom message
            button(@click="subscribeMd") market data
            button(@click="sendWs('sor')") orders
            button(@click="sendWs('spl')") account pnl
            button(@click="subscribeMh") market history
            button(@click="sendWs('spd')") portfolio
            button(@click="secdef") secdef
            button(@click="bookdata") bookdata
        div
            button(@click="clearLog") clear log
        div(class="stream-log", v-html="streamLog")
        div(style="float: right")
            label(for="max-buffer") max buffer size (for console debug)
            span &nbsp;
            input(id="max-buffer", size="5", style="text-align: right", v-model="maxBuffer")
</template>

<script>

    import mxGlobal from '../mixins/mx-global'
    import mxOauth from '../mixins/mx-oauth.js'

    export default {
        name: 'streaming-api-view',
        mixins: [mxGlobal, mxOauth],
        data() {
            return {
                ws: undefined,
                streamLog: '',
                connected: undefined,
                maxBuffer: 10000
            }
        },
        computed: {
        },
        methods: {
            sendWs(msg) {
                this.ws && this.ws.send(msg);
                this.streamLog = '-> ' + msg + '<br>' + this.streamLog;
            },
            disconnect() {
                this.ws.close();
            },
            clearLog() {
                this.streamLog = '';
            },
            sendSession() {
                var options = this.getOptions('/tickle');
                this.sendProtectedResourceRequest(options, 'GET', {})
                    .then((res) => {
                        const logon = { session: res.session };
                        console.log(logon);
                        this.sendWs(JSON.stringify(logon));
                    })
                    .catch((res) => res.json().then((e) => {
                        this.streamLog = '-> ' + JSON.stringify(e, null, 2) + '<br>' + this.streamLog
                    }));
            },
            connect() {
                // forces the browser to negotiate the session with the backend
                const wsUrl = this.wsBaseUrl;
                window.ws = this.ws = new WebSocket(wsUrl);
                ws.binaryType = 'arraybuffer';
                ws.onopen = () => {
                    this.streamLog = 'e: open <br>' + this.streamLog;
                    this.connected = true;
                };
                ws.onmessage = async (event) => {
                    const msg = '<- ' + String.fromCharCode.apply(null, new Uint8Array(event.data));
                    this.streamLog = (msg + '<br>' + (this.streamLog.length > this.maxBuffer ? '' : this.streamLog));
                };
                ws.onclose = (e) => {
                    this.streamLog = 'e: closed <br>' + this.streamLog;
                    this.connected = false;
                }
            },
            toggleWs() {
                if (this.connected) {
                    this.disconnect();
                } else {
                    this.connect();
                }
            },
            customWsRequest() {
                const req = prompt('Enter WS message to send:');
                this.sendWs(req);
            },
            subscribeMd() {
                const conid = prompt('conid?', 8314);
                this.sendWs('smd+' + conid + '+{"fields":["31","83"],"tempo":1000}');
            },
            subscribeMh() {
                const conid = prompt('conid?', 8314);
                this.sendWs('smh+' + conid + '+{"period":"1d"}');
            },
            secdef() {
                const conid = prompt('conid?', 8314);
                this.sendWs('sdr+' + conid);
            },
            bookdata() {
                const acctId = prompt('account id?');
                const conid = prompt('conid?', 8314);
                const exch = prompt('(optional, can leave blank) exchange?', '');
                var toSend = 'sbd+' + acctId + '+' + conid;
                if (exch.length > 0) {
                    toSend = toSend + '+' + exch;
                }
                this.sendWs(toSend);
            }

        }
    }
</script>

<style>
    .stream-log {
        margin: 2em 0 0 0;
        border: 1px solid #CACACA;
        height: 20em;
        overflow-x: auto;
        white-space: pre;
        font-family: "Lucida Console", Monaco, monospace;
        font-size: 0.8em;
    }
</style>