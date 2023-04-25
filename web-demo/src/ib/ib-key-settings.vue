<template lang="pug">
    div(class="key-settings")
        a(href="", @click.prevent="open('encryption')") Encryption Key
        a(href="", @click.prevent="open('sign')") Sign Key
        a(href="", @click.prevent="open('prime')") Prime
        a(href="https://www.interactivebrokers.com/webtradingapi/oauth.pdf",
            class="oauth-note",
            target="_tab") OAuth Instructions
        div(v-if="show == 'encryption'", class="ib-modal")
            div
                pre
                    | openssl genrsa -out private_encryption.pem 2048
                    | openssl rsa -in private_encryption.pem -outform PEM -pubout -out <b>public_encryption.pem</b>
            textarea(v-model="keys.privateEncryptionKey", :cols="70", rows="20")
        div(v-else-if="show == 'sign'", class="ib-modal")
            div
                pre
                    | openssl genrsa -out private_signature.pem 2048
                    | openssl rsa -in private_signature.pem -outform PEM -pubout -out <b>public_signature.pem</b>
            textarea(v-model="keys.privateSigningKey", :cols="70", rows="20")
        div(v-else-if="show == 'prime'", class="ib-modal")
            div
                pre
                    | openssl dhparam -outform PEM 2048 -out <b>dhparam.pem</b>
                    | openssl asn1parse < dhparam.pem
            textarea(v-model="keys.prime", :cols="70", rows="20")
</template>

<script>

    import {mapState} from "vuex";

    export default {
        name: 'key-settings',
        data() {
            return {
                show: '',
                cols: 70
            }
        },
        computed: {
            ...mapState(['oauth', 'session', 'credentials', 'settings', 'keys'])
        },
        methods: {
            open(val) {
                if (this.show == val) {
                    this.show = "";
                } else {
                    this.show = val;
                }
            }
        }
    }

</script>

<style>
    .key-settings a {
        margin-right: 1em;
    }

    .oauth-note {
        float: right;
    }
</style>