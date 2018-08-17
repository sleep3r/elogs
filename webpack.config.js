const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const Cleaner = require('webpack-cleanup-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
// const CleanWebpackPlugin = require('clean-webpack-plugin');
// const HtmlWebpackTemplate = require('html-webpack-template');

module.exports = {
    mode: 'development',
    context: path.join(__dirname, 'assets'),
    entry: {
        messages: './notifications/index',
        leaching: './leaching/index',
        furnace: './furnace/index',
        index: './js/index',
    },
    output: {
        path: path.resolve('./static/webpack_bundles'),
        filename: "[name].js"
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader',
                ]
                // loader: 'css-loader'
            },
            {
                test: /\.scss$/,
                loader: 'sass-loader'
            },
            {
                test: /\.((ttf)|(woff)|(woff2)|(svg)|(eot))$/,
                loader: 'file-loader'
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    plugins: [
        new webpack.ProvidePlugin({
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            $: 'jquery',
            moment: 'moment',
        }),
        new webpack.HotModuleReplacementPlugin(),
        new BundleTracker({filename: './webpack-stats.json'}),
        new Cleaner(),
        new HtmlWebpackPlugin(),
    ],
    devtool: 'inline-source-map',
    devServer: {
        hot: true,
        clientLogLevel: 'warning',
        historyApiFallback: true,
        headers: {"Access-Control-Allow-Origin": "*"},
        host: '127.0.0.1',
        port: '8001',
        open: false,
        proxy: {
            "/": "http://127.0.0.1:8000"
        },
        publicPath: "/static/webpack_bundles"
    }
};
