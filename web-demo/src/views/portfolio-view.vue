<template lang="pug">
    div
        button(@click="getPortfolio") Get Positions
        positions(:positions="positions", class="w100")
</template>

<script>
    import mxOauth from '../mixins/mx-oauth';
    import mxGlobal from '../mixins/mx-global';

    export default {
        name: 'portfolio',
        mixins: [mxOauth, mxGlobal],
        data() {
            return {
                positions: [],
                accounts: []
            }
        },
        methods: {
            getPortfolio: function () {
                this.sendProtectedResourceRequest(this.getOptions('/portfolio/accounts'), 'GET', {}).then(function (res) {
                    this.accounts = res;
                    this.getPositions();
                }.bind(this));
            },
            getPositions() {
                this.positions = [];
                for (const account of this.accounts) {
                    const ep = `/portfolio/${account.id}/positions`;
                    this.sendProtectedResourceRequest(this.getOptions(ep), 'GET', {}).then(function (res) {
                        this.positions = this.positions.concat(res);
                    }.bind(this));
                }
            },
            positionsSnapshotUpdating: function() {
                for (var i = 0; i < this.positions.length; i++) {
                    const options = this.getOptions('/iserver/marketdata/snapshot');
                    options['url'] = options['url'] + '?conids=' + this.positions[i].ContractId;
                    this.sendProtectedResourceRequest(options, 'GET', {}).then(function(idx, res) {
                        this.positions[idx].Bid = res[0].Bid.price;
                        this.positions[idx].Offer = res[0].Offer.price;
                        this.positions[idx].Trade = res[0].Trade.price;
                        this.positions[idx].Closing = res[0].Closing.price;
                        this.positions[idx].High = res[0].High.price;
                        this.positions[idx].Low = res[0].Low.price;
                        this.$forceUpdate();
                    }.bind(this, i));
                }
                setTimeout(this.positionsSnapshotUpdating, 5000);
            },
        }
    }
</script>

<style>

</style>