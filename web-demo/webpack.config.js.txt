const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin')

const envFeatures = require("./build/env." + process.env.BUILD_ENV + '.json');
const features = {};

Object.assign(features, envFeatures);
Object.assign(process.env, features); // override process.env

const contentBase = path.resolve(__dirname, './dist');
const isProd = process.env.NODE_ENV == 'production';

console.log('Production     : ' + isProd);
console.log('Base URL       : ' + (process.env.BASE_URL));
console.log('Public path    : ' + features.PUBLIC_PATH);
console.log('BUILD_FEATURES : ' + JSON.stringify(features));
console.log('content base   : ' + contentBase);

const webpackEnv = {
    NODE_ENV: JSON.stringify(process.env.NODE_ENV),
    BUILD_FEATURES: JSON.stringify(features),
    BUILD_TIME: JSON.stringify(new Date()),
    RANDOM_NUMBER: JSON.stringify(Math.random().toString(16).slice(2))
};

var keys = Object.keys(features).forEach(k => {
    webpackEnv[k] = JSON.stringify(features[k]) // changes 'hello', to '"hello"'
})


const config = {
    mode: isProd ? 'production' : 'development',
    output: {
        filename: '[name].js',
        chunkFilename: 'part.[name].[chunkhash].js',
        publicPath: '',
        path: contentBase
    },
    entry: {
        index: ['./src/main.js'],
        vendor: ['vue', 'vuex']
    },
    resolve: {
        alias: {
            'vue': 'vue/dist/vue.js',
            'vuex': 'vuex/dist/vuex.js',
            'vue-router': 'vue-router/dist/vue-router.js'
        }
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'src/index.html',
            inject: false,
            title: 'IBKR OAuth Demo',
            portalBaseUrl: process.env.PORTAL_BASE_URL,
            env: process.env.NODE_ENV
        }),
        new VueLoaderPlugin(),
        new webpack.ProvidePlugin({
            Vue: ['vue/dist/vue.js', 'default']
        })
    ],
    module: {
        rules: [{
            test: /\.vue$/,
            loader: 'vue-loader'
        },
            {
                test: /\.css$/i,
                use: ['vue-style-loader', 'css-loader'],
            },
            {
                test: /\.pug$/,
                oneOf: [
                    {
                        resourceQuery: /^\?vue/,
                        use: ['pug-plain-loader']
                    },
                    {
                        use: ['pug-loader']
                    }
                ]
            },
            {
                test: /\.less$/i,
                use: ['vue-style-loader', 'css-loader', 'less-loader'],
            }]
    },
    devServer: {
	    contentBase: path.resolve(__dirname, ''),
	    disableHostCheck: true
    }
}

if (isProd) {
    config.optimization = {
        minimize: true
    };
    config.plugins.push(
        new webpack.LoaderOptionsPlugin({
            minimize: true
        }));
}

module.exports = config;