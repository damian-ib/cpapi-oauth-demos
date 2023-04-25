<template lang="pug">
div(class="ib-positions")
    h5 Positions
    table(class="w100")
        thead
            tr
                th ContractId
                th Ticker
                th SecurityType
                th AverageCost
                th Position
                th Currency
                th Bid
                th Offer
                th Trade
                th Closing
                th High
                th Low
        tbody
            tr(v-for="row in positions")
                td {{ row.conid }}
                td {{ row.contractDesc }}
                td {{ row.assetClass }}
                td {{ row.avgCost }}
                td {{ row.position }}
                td {{ row.currency }}
                td {{ row.Bid }}
                td {{ row.Offer }}
                td {{ row.Trade }}
                td {{ row.Closing }}
                td {{ row.High }}
                td {{ row.Low }}
</template>

<script>
export default {
    name: 'ib-positions',
    props: {
        positions: Array
    }
}
</script>

<style>
    .ib-positions table {
        border-collapse: collapse;
        border-spacing: 0;
        border: 1px solid #CACACA;
    }
    .ib-positions tbody tr:nth-child(odd) {
        background-color: #f2f2f2;
    }
    .ib-positions thead {
        text-align: left;
        background-color: #CACACA !important;
    }
</style>