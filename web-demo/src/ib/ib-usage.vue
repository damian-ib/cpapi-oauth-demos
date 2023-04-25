<template lang="pug">
div(class="howto")
    h5 Pre-requisites
    br
    p 
        | A browser with CORS disabled. See README.md or how to
        |
        a(href="https://teckangaroo.com/chrome-disable-web-security/") disable web security in Chrome
    br
    h5 Usage
    ul
        li Generate a request token by pressing "GET" on the Request Token step.
        li Go to the /authorize link that will be shown once the request token is generated.
            ul
                li
                    p
                        | Login with an IB account
                        br
                        | <u>Note:</u> Only paper users are supported if using TESTCONS consumer key.
                li
                    p
                        | Once you are authenticated and sign the agreement you will be redirected to an empty page.
                        br
                        | Look at the URL and copy the text after oauth_verifier to the "Verifier Token" input box
                        br
                        | <u>Note</u>: In production the user would be redirected to a callback page registered with us for that specific consumer.
        li
            | Once you copy the Verifier Token, click on "GET" on the Access Token step.
            br
            | <u>Note</u>: At this stage, you can store the access token and access token secret.
            | The authorize step is no longer needed to access the API as the authorized user.
            | By restoring the access token and access token secret you can start at Step 4. (LST) below.
        li
            | "GET" Live Session Token (LST)
        li
            | Once you get the Live Session Token you can try the API calls.
</template>

<script>
export default {
    name: 'ib-usage'
}
</script>

<style>
    .howto {
        padding: 1em;
    }
</style>