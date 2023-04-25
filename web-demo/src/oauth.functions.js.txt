const crypto = require('crypto')
const fetch = require('node-fetch')
const bigInteger = require('big-integer')

const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

function trim(input) {
    if (input.length == 0 || input[0] != 0)
        return input;
    var len = input.length;
    var i = 1;
    while (input[i] == 0 && i < len)
        i += 1;
    var ret = [];
    for (; i < len; i += 1) {
        ret.push(input[i]);
    }
    return ret;
}

export function objectBodyToPayload(body) {
    var payload = '';
    for (var i = 0; i < body.length; i++) {
        const key = body[i].key;
        const value = body[i].value;
        if (value && Array.isArray(value)) {
            var valString = '';
            value.forEach((function (item, i) {
                valString += key + '=' + item;
                if (i < value.length) {
                    valString += '&';
                }
            }).bind(this));
            payload += valString;
        } else {
            payload += key + '=' + value + '&';
        }
    }
    payload = payload.substr(0, payload.length - 1);
    return payload;
}

export function toByteArray(x) {
    var hexString = x.toString(16);
    if (hexString.length % 2 > 0) hexString = "0" + hexString;
    var byteArray = [];
    if (x.toString(2).length % 8 == 0) {
        byteArray.push(0);
    }
    for (var i = 0; i < hexString.length; i += 2) {
        byteArray.push(parseInt(hexString.slice(i, i + 2), 16));
    }
    return byteArray;
}

export function calculateLST(dhResponse, dhRandom, accessTokenSecret, prime) {
    if (accessTokenSecret instanceof String) {
        accessTokenSecret = Buffer.from(accessTokenSecret, 'hex');
    }
    console.log(accessTokenSecret);
    var B = bigInteger(dhResponse, 16);
    var a = bigInteger(dhRandom, 16);
    var K = B.modPow(a, bigInteger(prime, 16));
    return crypto
        .createHmac('sha1', toByteArray(K))
        .update(accessTokenSecret)
        .digest('base64');
}

export function verifyLST(lst, consumerKey, lstSignature) {
    var toVerify = crypto
        .createHmac('sha1', Buffer.from(lst, 'base64'))
        .update(Buffer.from(consumerKey, 'utf8'))
        .digest('hex');
    console.log(toVerify);
    console.log(lstSignature);
    return toVerify == lstSignature;
}

export function compute_sk(seed, verifier) {
    const hash = crypto.createHash('sha1');
    hash.update(Buffer.from(seed + verifier, 'hex'));
    return hash.digest('hex');
}


