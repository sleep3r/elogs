// const ServiceWorkerWebpackPlugin = require('serviceworker-webpack-plugin');
const path = require('path');
const webpack = require('webpack');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const SWPrecacheWebpackPlugin = require('sw-precache-webpack-plugin');
// const CompressionPlugin = require('compression-webpack-plugin');
// const TerserPlugin = require('terser-webpack-plugin');

const PUBLIC_PATH = 'https://elogs.club/';

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
        //         entry: path.join(__dirname, 'src/e-logs-sw.js'),
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
        plugins: [
            new SWPrecacheWebpackPlugin(
                {
                    cacheId: 'e-logs-cache-v1',
                    dontCacheBustUrlsMatching: /\.\w{8}\./,
                    staticFileGlobs: ['dist/**/*.{js,html,css}'],
                    stripPrefix: 'dist/',
                    filename: 'service-worker.js',
                    minify: true,
                    navigateFallback: PUBLIC_PATH + 'index.html',
                    staticFileGlobsIgnorePatterns: [/\.map$/, /asset-manifest\.json$/],
                    importScripts: [
                        {
                          filename: './public/e-logs-sw.js'
                        }
                    ]
                }
            ),
        ],
    },

    baseUrl: undefined,
    outputDir: undefined,
    assetsDir: undefined,
    runtimeCompiler: true,
    productionSourceMap: undefined,
    parallel: undefined,
    css: undefined
};
