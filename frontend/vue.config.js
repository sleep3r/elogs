// const ServiceWorkerWebpackPlugin = require('serviceworker-webpack-plugin');
// const path = require('path');
const webpack = require('webpack');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
// const CompressionPlugin = require('compression-webpack-plugin');
// const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
    configureWebpack: {
        module: {
            rules: [
                {
                    test: /\.(pdf)$/,
                    loader: 'file-loader'
                },
            ]
        },
        // optimization: {
        //     minimizer: [new UglifyJsPlugin(
        //     )]
        // },
        // plugins: [
        // ]
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
        //     new CompressionPlugin({
        //         algorithm: "gzip",
        //         test: /\.js$|\.css$|\.html$/,
        //         threshold: 10240,
        //         minRatio: 0.8
        //     })
        // ])
        //     : (module.exports.plugins || [])
    },

    baseUrl: undefined,
    outputDir: undefined,
    assetsDir: undefined,
    runtimeCompiler: true,
    productionSourceMap: undefined,
    parallel: undefined,
    css: undefined
};
