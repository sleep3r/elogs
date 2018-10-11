// const ServiceWorkerWebpackPlugin = require('serviceworker-webpack-plugin');
// const path = require('path');
// const webpack = require('webpack');
// const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
// const CompressionPlugin = require('compression-webpack-plugin');
// const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
    configureWebpack: {
        module: {
            rules: [
                {
                    test: /\.(pdf)$/,
                    loader: 'file-loader',
                }
            ]
        },
        // plugins: [
        //     new ServiceWorkerWebpackPlugin({
        //         entry: path.join(__dirname, 'src/sw2.js'),
        //         excludes: [],
        //         includes: ['**/.*', '**/*.map']
        //     }),
        // ]
        // plugins : process.env.NODE_ENV === 'production' ?
        //     (module.exports.plugins || []).concat([
        //     new webpack.DefinePlugin({
        //         'process.env': {
        //             'NODE_ENV': JSON.stringify('production')
        //         }
        //     }),
        //     // new UglifyJsPlugin({
        //     //     include: /\.js$/, cache: true, parallel: true,
        //     //     extractComments: true, sourceMap: true
        //     // }),
        //     new CompressionPlugin({
        //         algorithm: "gzip",
        //         test: /\.js$|\.css$|\.html$/,
        //         threshold: 10240,
        //         minRatio: 0.8
        //     })
        // ])
        //     : (module.exports.plugins || [])
    }
}
