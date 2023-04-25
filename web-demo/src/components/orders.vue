<template lang="pug">
div
    h5 Orders
    table
        thead
            tr
                th CustomerOrderId
                th ContractId
                th Ticker
                th ListingExchange
                th RemainingQuantity
                th FilledQuantity
                th OrderType
                th TimeInForce
                th OutsideRTH
                th Side
                th Price
                th Status
                th Warning
                th TransactionTime
        tbody 
            tr(v-for="row in orders")
                td {{ row.CustomerOrderId }}
                td {{ row.ContractId }}
                td {{ row.Ticker }}
                td {{ row.ListingExchange }}
                td {{ row.RemainingQuantity }}
                td {{ row.FilledQuantity }}
                td {{ row.OrderType }}
                td {{ row.TimeInForce }}
                td {{ row.OutsideRTH }}
                td {{ row.Side }}
                td {{ row.Price }}
                td {{ row.Status }}
                td {{ row.Warning }}
                td {{ row.TransactionTime }}
</template>

<script>
export default {
    name: 'ib-orders',
    props: {
        orders: Array
    }
}
</script>