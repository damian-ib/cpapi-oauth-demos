# IBKR Client Portal API OAuth Demo

The IBKR OAuth web demo represents the entire OAuth flow. It is meant to be demonstration of the steps required to integrate OAuth with your client application. Please note that the whole process may not be applicable depending on your use case. For example, clients using OAuth for in-house use will only need to integrate the live session token and brokerage initiation steps in their app.

## Pre-requisites

- NodeJS: https://nodejs.org/ (Please use version 16.X.Y, there are known incompatibilities with more recent versions of the demo)
- A browser with CORS disabled must be used if running locally. For Chrome, use the --disable-web-security option along with the --user-data-dir option. Alternatively you may use a CORS browser extension.

## Quickstart

### Building the Demo

1. Run "npm install" in root project directory to install project dependencies.  
2. Once installed, run "npm run demo" to run the demo inside webpack dev server. The demo will be available under http://localhost:20000.


### Using the demo

1. Press the GET button next to the request token field. If you are not seeing a response, check if you have disabled CORS as per the pre-requisites list.
2. Click on the Authorize User link that appeared under the request token field. A new tab will be opened with the IBKR login form. Use your paper login credentials to authenticate the request token. 
3. On successful login the user will be redirected back to an empty instance of the web app. The difference is that the URL will now contain the query params, `oauth_token` and `oauth_verifier`. Copy the value of the `oauth_verifier` query parameter and navigate to the tab that contains the demo we started in previous steps.
4. Paste the `oauth_verifier` value into the verifier token field.
5. Click GET next to the to Access Token field to get the access token and access token secrets.
6. Click on GET next to the Live Session Token field to generate the live session token.
7. Finally, click on the REST API link and press the Start Session button to initiate the brokerage session. A brokerage session is required in order to access protected including order placement, market data requests, portfolio data, etc. If all is working you'll see the following response at the bottom of the screen:
```json
{
	"passed": true,
	"authenticated": true,
	"connected": true,
	"competing": false
}
```

You are now ready to call other endpoints.