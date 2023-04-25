import {mapState} from "vuex";

export default {
    computed: {
        ...mapState(['oauth', 'session', 'credentials', 'settings', 'keys', 'output']),
        baseUrl() {
            return this.session.useGw ? this.session.gwBaseUrl : this.session.baseUrl;
        },
        wsBaseUrl() {
            return this.baseUrl.replace('https', 'wss') + '/ws';
        },
        showRestApi() {
            if (this.session.useGw && this.session.gwBaseUrl) {
                return true;
            }
            return this.credentials.liveSessionToken.length > 0 && this.credentials.accessToken.length > 0;
        }
    },
    methods: {
        apiGet(endPoint, baseUrlOverride) {
            var options = this.getOptions(endPoint);
            if (baseUrlOverride) {
                options.url = baseUrlOverride + endPoint;
            }
            this.sendProtectedResourceRequest(options, 'GET', {})
                .then((res) => this.handleApiResponse(res))
                .catch((res) => res.json().then((e) => this.handleApiError(res, e)));
        },
        getOptions: function (endPoint) {
            const options = {...this.credentials}; // copy
            options.useGw = this.session.useGw;
            if (endPoint) {
                options.endPoint = endPoint;
                options.url = this.baseUrl + endPoint;
            }
            return options;
        },
        handleApiError(res, e) {
            console.error(res);
            this.output.value = 'status ' + res.status + '\n' + JSON.stringify(e, null, 2);
        },
        handleApiResponse(res) {
            console.debug(res);
            this.output.value = 'status 200\n' + JSON.stringify(res, null, 2);
        }
    }
}