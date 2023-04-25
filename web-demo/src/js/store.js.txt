import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        session: {
            isDev: false,
            useGw: false,
            baseUrl: 'https://api.ibkr.com/v1/api',
            gwBaseUrl: 'https://localhost:5000/v1/api'
        },
        settings: {
            machineId: 'CCCCCCCC',
            mac: '48-DF-37-57-33-80'
        },
        credentials: {
            consKey: 'TESTCONS',
            realm: 'test_realm',
            accessToken: '',
            liveSessionToken: ''
        },
        oauth: {
            requestToken: '',
            verifier: '',
            tokenSecret: ''
        },
        keys: {
            privateSigningKey: `-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC8i4AoB+OIQzz6
EkYvXZLmKK8f6XAD3izc/PzRP1t05cTogcNZYFEYSfj2PyCOYSjPhw+fWPxbwJpM
0WBv7i9Lh90zuFIJJZowb0HSuKlQrGKqK0brpjEUZ++jwFx0jvoDziHDszoSGbSn
ekWEzldNQOlPMi6UOlSCb9RczkPdJ7hJy3fY1qNDaX/FnWcVGylF11FCl9yU+yen
lXG/qQiMPgG5NyTrG7j2sZvzMpyMmeW/osFtXjy1oGL3fRYd8UOXeEFncUedPYm4
PSf3qmhMIK4wQX4YBlO4gfbyMXCImRZFJ++O2SkojgETVA1qPb2/p4tc+vncrJQC
dO7JaHypAgMBAAECggEAX7/wa2PmNxL+anjRT8iTi3LpzKj+C9jOq8OGmLU2Ot1c
7D7J+B+jz1PxrQxN+kB5Ozr5whCsx+O9+Hj0IqOxPQhYW6Wlc6O29BXsNZk10xRY
Xtbvg0i48AYAewZ7bW4WpcwO9ZWVTg/j4JGFsHYhe8gVM/TmFrywojUsgZz2dd6Q
ZPukktlVcgJHvD6eEcQVxm/nL6FGBzOVcGORqTl5qdwVB81LelknNszrPq88xvME
vWT3ve0m2SwLysX1RfcfVCW6iwgJVcU9ssuwQco3NlUHl5CDATHEbeFqwalj2P7I
EL2ELLgMoOh6DVYMHvRRB1psf9hNXhrhx3orceqYCQKBgQDqrT0yWI0QOe++Pi/P
EjiPRerK5/BVHBUXmmTxpRKieELw/kSWPIFY/u9lMsH4VVo0Asyjzh1LTmkn0z2i
XDARN70YH0rcHFv8Jz1Iszg2NWz8DgeyacEtNyX2yPzn+2rq9ZXdgrSQNBciq78d
6o22iK9jA6oTI8EfNaxPkRyruwKBgQDNrTNbdxqi7vTL9ILaBQ2WTbjC+C4L+9UP
DUI05vta5jNosfIOI3+z8p6Vu9I5b6mRNp2t+cuTKQM6CwVBXEfi7DzTODk3Su0Q
Z4egB25D3jYOzOwiZp9RLrBIcMy+UISCen6Ko2yo4pR5mMM+n/Gf1r+jmdgtFY70
e1fClhsI6wKBgEZGFEJERBGs177nTle6xBcbP8D9DXnfC+3ifQHjhZ4DV0BlU9KN
Ucp9pOBv/6fGn1ld0TvoF9uaImEbn6RD6NzvDP/xNvCMyXrLoU1o5ZdODlG4PdPO
WVuZ3RN2gk1Re2XansMTRdC82IS4W2Ww/DjB24tR6JcMqOMYpn25HZXLAoGAHj2t
I3GrtPE1hRd6ddvwV30uAVzESHbKqN/mMCkWJBNc07P2RyXpDOhLcPCgxFkqsXM6
U+46hHSvSMV+DFIpL7BUcSn/H6YgnRzb0CfHiqsNf7eZsKUuH52hxcTwFbt5AEZK
fM/ylhJailZvvrF9sWa93qwsINTepAvOp4myh+kCgYA1XaXzGLwE0hF3zLJyho7U
oJvxPb/LAhjapONpq7y2EK+Ikl2RlSCfxRbdqWmv0tRKywfWTaiS+Uq9IeohAs3l
uXcDesPrBlG8GCnhVtIa2WNYfFJUwM+MGLC551PGqucnx3IjxoLgt1QEV9nc/38X
Ez6OZAESBCtWnxvsOKjkNA==
-----END PRIVATE KEY-----`,
            privateEncryptionKey: `-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDlpbiKR9DNDQeA
TjeORl4gt8re+pCCmcERVI/swWI+uYA4GE1DHXPAbTJl6aTToQmI8ufF15E+wQKP
XZcmXDxGXvJqwlQPEmVqNt1pJn4cfquCsx/cBqHOsJIkigXpex89FS8lOIWMjvcz
K8iZCnWnd/GKuVKp4qqxsOmiN765oX8sv2VQiTUrwcn3Byyqltz3VyEKcOeRq0ul
jHW7pHQHIFJYZd4xu7eDk7MbXNCY5CW3QBYBXEGd/inB14Z6PgEl5ItVun2th5P/
n9TByrey4L98NwN/UwenE6pMoLfUPihOcm6lTaYgjDwqZwQPo11rdchZXDiQ+cec
+5XA8qNvAgMBAAECggEBAM/Dqr2QU5vwGcU+/ow9pZM8NNKfJnbB3CZttvifzN6q
vRIDCoOZ9cs1/86sH29H1nSMLpyTdtirjkFejw0pjW6tH+zue1ZXcmEx2gbzyEzH
XSwWGtDZPzLcFJvyM38U4SJGNC0cgda00Xj+N7IeAGvO3DyBhgQlCgFQ6U7V2Dvf
5Vrn2VhepS8GiT3gzzZ2zZ/ARVwZiMbz8uCc98GX4ks7LLF/zXv4p8ZLMP11cHIq
vdACyPZXC3l3zH83XNW5YjO0Ht3iMEdM1etYI4l0YOrHQTjWCn8YieOGWdbbvOXx
dyPcgjMC7rdNB6VeHuNYzzlNn/m3WOqPpc+v/lIbzWECgYEA+g2AR5c2sj2/KLU0
HdjhqWzekdRXuAIc6pW0OhJjdiXaAi1S+ltN3ybwVXYw2TANxuo8Uw49vuF7RQmj
KfoRn9oxnB/zaS3ZbhFJPxjEEmKM3W7c7EaAxIgjU/t/34UdPOEYtHyQ7QDlgzy3
5pmpnTycFUUSsxGU1wtffXJvm3MCgYEA6xv6K94S6jeVaQ6pFgG+2upHfT+aFrTb
cwVPcw3Aka8zhfIP1mb00JyqCQjP0gDfa41EUHV+bEhWCJgz9sF2oEa/5LffGAzP
RIQmiwPIV0ocDDESBiL2CtYOc3JrP0Sv4TtaojUC+M60qgftcWxouDZTKDpEkh01
lR/krIwW0RUCgYEAs6CVQVhwM1TGCNE68iIF4bbSoEHBDe9+pEoMoRbqmkoQtTWo
AS8r3p1TUqFH8A1kKDvGQAff9Up3Sh3lN1dr58BPmQ8exbTpF/eU/Z2l5GslNEDa
tWTkRcpiTodB0ekHGt+85pMBbTASr9cjaKWEQe7zVRg8maSMnnqOC0j0wd8CgYBa
1IEvB2mZUQYJA1/xn5UDcDVUPwkhspeBdVC/a1W1MtGd8umJdFcqbQwH136qbCnk
nDwDNZE09jE+usaAkzdoLk0eaKbo3LIKj19wn3J7vqbdUuvasRELGK2WjmK+m6Oz
SUH3nrFaPElx0wQ5qJ9AY8R2qyQoqt4zkZG/05NRDQKBgCIe30lebp9p/9k5pcc9
g5Nm2poiEMxkwml83YmGSuSJif2FwfXjK8H6OnyugZXiwRUiswvlH6Gc6ERY73HH
CTsDq0Jt9MXUTp2DCE/UKbKZ2gZ2QZIyPz9yCWU/HHb367Dhh+f0hKr5fgxMFSDV
UVV09g9GfiIkDMwRS96ugq1N
-----END PRIVATE KEY-----`,
            generator: 2,
            prime: `\
f51d7ab737a452668fd8b5eec12fcdc3c01a0744d93db2e9b1dc335bd2551ec6\
7e11becc60c33a73497a0f7c086d87e45781ada35b7af72708f31ae221347a1c\
6517575a347df83a321d05450547ee13a8182280ed81423002aa6337b48a251d\
840bfdabe8d41b8109284933a6c33bc6652ea9c7a5fd6b4945b7b39f1d951ae1\
9b9192061e2f9de84768b67c425258724cdb96975917cabdea87e7e0bc72b01a\
331d06f2f34229a5ec742b399fcffa510bf6b8f9b5bf9858f058371a49aa4f95\
0f7fbfb3f47710af34baa83fff1b467d38d0e6b1b0a2d117f178cf930d7dfdcc\
8f6755a2229d48492a967f493041121e382b9e87ca1368c09f54e6352d909f2b`
        },
        output: {
            value: ''
        }
    }
});