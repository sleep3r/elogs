const ServiceWorkerWebpackPlugin = require('serviceworker-webpack-plugin');
const path = require('path');

module.exports = {
    configureWebpack: {
        module: {
            rules: [
                {
                    test: /\.pdf$/,
                    loader: 'file-loader',
                }
            ]
        },
        plugins: [
            new ServiceWorkerWebpackPlugin({
                entry: './src/sw2.js'
            }),
        ]
    }
}