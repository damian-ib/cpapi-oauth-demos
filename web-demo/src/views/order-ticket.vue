<template lang="pug">
    ///--Use contract/info
    div
        form
            fieldset
                legend Order Form
                p
                    label Account Id
                    input(v-model="orderForm.acctId")
                p
                    label Customer Order Id
                    input(v-model="orderForm.cOID")
                p
                    label Contract Id
                    input(v-model.number="orderForm.conid" type="number")
                p(v-if="false")
                    label Ticker
                    input(v-model="orderForm.ticker")
                p(v-if="false")
                    label Listing Exchange
                    input(v-model="orderForm.listingExchange")
                p
                    label Security Type
                    input(v-model="orderForm.secType")
                p(v-if="false")
                    label Contract Id
                    input(v-model="orderForm.ContractId")
                p
                    label Quantity
                    input(v-model.number="orderForm.quantity" type="number")
                p
                    label Price
                    input(v-model.number="orderForm.price" type="number")
                p
                    label Order Type
                    select(v-model="orderForm.orderType")
                        option LMT
                        option MKT
                        option STP
                        option STP_LIMIT
                p(v-if="orderForm.orderType == 'STP_LIMIT'")
                    label Aux Price
                    input(v-model="orderForm.AuxPrice")
                p
                    label Time In Force
                    select v-model="orderForm.tif">
                        option DAY
                        option GTC
                p(v-if="false")
                    label Outside RTH
                    select(v-model="orderForm.outsideRTH")
                        option true
                        option false
                p
                    label Side
                    select(v-model="orderForm.side")
                        option BUY
                        option SELL
                p(v-if="false")
                    label Order Restrictions
                    input(v-model="orderForm.OrderRestrictions")
                p
                    button(type = "button" v-on:click="placeOrder")
                        b Place Order
                    button(type = "button" v-on:click="cancelOrder")
                        b Cancel Order
                    button(type = "button" v-on:click="modifyOrder")
                        b Modify Order
                    button(type = "button" v-on:click="refresh")
                        b Refresh
            ib-orders(class="before-lg")
        div(class="before-md", class="w100")
            h5(v-if="output.value.length > 0") Output
            pre(class="w100") {{ output.value }}
</template>

<script>
    import mxGlobal from '../mixins/mx-global.js'
    import mxOauth from '../mixins/mx-oauth.js'

    export default {
        name: 'order-ticket',
        mixins: [mxGlobal, mxOauth],
        data() {
            return {
                orderForm: {
                    acctId: '',
                    cOID: '1',
                    conid: 8314,
                    //ticker: 'IBM',
                    //listingExchange: 'NYSE',
                    secType: 'STK',
                    quantity: 100,
                    price: 150.00,
                    orderType: 'LMT',
                    tif: 'DAY',
                    outsideRTH: true,
                    side: 'BUY'
                }
            }
        },
        methods: {
            refresh: function() {
                console.log(this.positions);
                this.populateOrdersTable();
            },
            populateOrdersTable: function () {
                const ep = `/iserver/account/orders`;
                this.sendProtectedResourceRequest(this.getOptions(ep), 'GET', {}).then(function (res) {
                    this.output.value = res;
                }.bind(this));
            },
            placeOrder: function () {
                if (!this.orderForm.acctId) {
                    alert('Enter account id in order form');
                    return;
                }
                const ep = `/iserver/account/${this.orderForm.acctId}/order`;
                this.sendProtectedResourceRequest(this.getOptions(ep), 'POST', this.orderForm, 'json').then(function (res) {
                    this.handleConfirmation(res);
                }.bind(this));
            },
            handleConfirmation: function(res) {
                if (res[0].id) {
                    var message = res[0].message[0];
                    var confirmedOrder = confirm(message);
                    const ep = `/iserver/reply/${res[0].id}`;
                    this.sendProtectedResourceRequest(this.getOptions(ep), 'POST', {confirmed: confirmedOrder}, 'json').then(function (res1) {
                        this.handleConfirmation(res1);
                    }.bind(this));
                } else {
                    this.handleApiResponse(res);
                }
            },
            cancelOrder: function () {
                if (!this.orderForm.acctId) {
                    alert('Enter account id in order form');
                    return;
                }
                const orderId = prompt('Enter order ID to cancel');
                const ep = `/iserver/account/${this.orderForm.acctId}/order/${orderId}`;
                this.sendProtectedResourceRequest(this.getOptions(ep), 'DELETE', {}).then(function (res) {
                    this.handleApiResponse(res);
                }.bind(this));
            },
            modifyOrder: function () {
                if (!this.orderForm.acctId) {
                    alert('Enter account id in order form');
                    return;
                }
                const orderId = prompt('Enter order ID to modify');
                const ep = `/iserver/account/${this.orderForm.acctId}/order/${orderId}`;
                this.sendProtectedResourceRequest(this.getOptions(ep), 'PUT', this.orderForm, 'json').then(function (res) {
                    this.handleApiResponse(res);
                }.bind(this));
            }
        }
    }
</script>
