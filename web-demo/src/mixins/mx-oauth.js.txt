const OAuth = require('oauth-1.0a')
const crypto = require('crypto')

import {
    objectBodyToPayload
} from "../oauth.functions";

export default {

    methods: {
        sendProtectedResourceRequest(options, method, body, bodyType) {
            return new Promise((resolve, reject) => {
                this.oauthRequest(options, 'protectedResource', method, body, bodyType)
                    .then((res) => resolve(res))
                    .catch((err) => reject(err));
            });
        },

        /**
        @options: Options to specify, usually just use getOptions(endpoint)
        @requestType: Type of request e.g. protectedResource, sso
        @httpMethod: Http method e.g. GET, POST, DELETE, PUT
        @bodyType: Post body will default to urlencoded, can specify 'json' here
        **/
        oauthRequest(options, requestType, httpMethod, requestBody, bodyType) {
            var signatureMethod = '';
            if (requestType == 'protectedResource') {
                options.key = options.liveSessionToken;
                signatureMethod = 'HMAC-SHA256';
            } else {
                options.key = this.keys.privateSigningKey;
                signatureMethod = 'RSA-SHA256';
            }
            return new Promise(function (resolve, reject) {
                const oauth = OAuth({
                    consumer: {
                        key: options.consKey,
                    },
                    realm: options.realm,
                    signature_method: signatureMethod,
                    hash_function(key, base_string) {
                        if (signatureMethod == 'HMAC-SHA256') {
                            return crypto.createHmac('sha256', key)
                                .update(base_string)
                                .digest('base64');
                        } else {
                            var sign = crypto.createSign('RSA-SHA256')
                            sign.update(base_string);
                            return sign.sign(key, 'base64');

                        }
                    }
                });

                oauth.getSignature = function (request_data, key, oauth_data) {
                    var buff_key = key;
                    if (signatureMethod == 'HMAC-SHA256') {
                        buff_key = Buffer.from(key, 'base64');
                    }
                    var base = this.getBaseString(request_data, oauth_data);
                    //We need | to encode to %7C and not %257C
                    base = base.replace(/%257C/g, '%7C');
                    base = base.replace(/%252C/g, '%2C'); // market data ,
                    base = base.replace(/%253A/g, '%3A'); // Encoding ':'
                    if (options.prepend) {
                        base = options.prepend + base;
                    }
                    console.log('signature base', base);
                    return this.hash_function(buff_key, base);
                }
                oauth.toHeader = function (oauth_data) {
                    var sorted = this.sortObject(oauth_data);
                    var header_value = 'OAuth ';
                    if (this.realm) {
                        header_value += 'realm="' + this.realm + '"' + this.parameter_seperator;
                    }
                    if (oauth_data.diffie_hellman_challenge) {
                        header_value += 'diffie_hellman_challenge="' + oauth_data.diffie_hellman_challenge + '"' + this.parameter_seperator;
                    }
                    for (var i = 0; i < sorted.length; i++) {
                        if (sorted[i].key.indexOf('oauth_') !== 0)
                            continue;
                        header_value += this.percentEncode(sorted[i].key) + '="' + this.percentEncode(sorted[i].value) + '"' + this.parameter_seperator;
                    }
                    return {
                        Authorization: header_value.substr(0, header_value.length - this.parameter_seperator.length) //cut the last chars
                    };
                }
                const oauth_data = {
                    oauth_consumer_key: options.consKey,
                    oauth_nonce: oauth.getNonce(),
                    oauth_signature_method: oauth.signature_method,
                    oauth_timestamp: oauth.getTimeStamp(),
                }
                if (requestType == 'requestToken') {
                    oauth_data.oauth_callback = 'oob';
                } else if (requestType == 'accessToken') {
                    oauth_data.oauth_token = options.requestToken;
                    oauth_data.oauth_verifier = options.verifier;
                } else if (requestType != 'requestToken') {
                    oauth_data.oauth_token = options.accessToken;
                }
                if (options.diffieHellmanChallenge) {
                    oauth_data.diffie_hellman_challenge = options.diffieHellmanChallenge;
                }
                const request_data = {
                    url: options.url,
                    method: httpMethod
                }
                if (!bodyType || bodyType == 'urlencoded') {
                    request_data.data = requestBody;
                }
                console.log('request_data', request_data);
                console.log('oauth_data', oauth_data);
                oauth_data.oauth_signature = oauth.getSignature(request_data, options.key, oauth_data);
                if (bodyType == 'json') {
                    request_data.data = requestBody;
                }
                //Don't include payload in base string calculation
                const request_body = {
                    method: request_data.method,
                }
                if (!options.useGw) {
                    request_body.headers = new Headers(oauth.toHeader(oauth_data));
                } else {
                    request_body.headers = new Headers();
                }
                if (requestBody) {
                    if (httpMethod == 'POST' || httpMethod == 'PUT') {
                        if (bodyType == 'json') {
                            request_body.body = JSON.stringify(request_data.data);
                            request_body.headers.append('Content-Type', 'application/json');
                        } else {
                            request_body.body = objectBodyToPayload(oauth.sortObject(request_data.data));
                            request_body.headers.append('Content-Type', 'application/x-www-form-urlencoded');
                        }
                    }
                }
                if (requestType == 'sso') {
                    request_body.body = JSON.stringify(requestBody);
                    request_body.headers.append('Content-Type', 'application/json');
                }
                request_body.credentials = 'include';

                console.log('sending oauth ' + httpMethod + ' request ' + request_data.url);
                fetch(request_data.url, request_body).then(function (res) {
                    if (res.status == 200) {
                        res.json().then(function (data) {
                            console.log(data);
                            resolve(data);
                        });
                    } else {
                        reject(res);
                    }
                }).catch(function (err) {
                    console.log(err);
                    reject(err);
                });
            });
        }
    }
}
