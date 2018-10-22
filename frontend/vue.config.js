const path = require('path');
const webpack = require('webpack');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const SWPrecacheWebpackPlugin = require('sw-precache-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ResourceHintWebpackPlugin = require('resource-hints-webpack-plugin');
// const ServiceWorkerWebpackPlugin = require('serviceworker-webpack-plugin');
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
        optimization: {
            splitChunks: {
                chunks: 'all'
            }
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
            new webpack.ProvidePlugin({
                $: 'jquery',
                jQuery: 'jquery',
                _: 'lodash'
                // Popper: ['popper.js', 'default'],
            }),
            new webpack.DefinePlugin({ PRODUCTION: JSON.stringify(false) }),
            new CopyWebpackPlugin([
                {
                    from: path.resolve(__dirname, './src/e-logs-sw.js'),
                    to: path.resolve(__dirname, './dist/e-logs-sw.js')
                }
            ]),
            new HtmlWebpackPlugin({
                inject: false,
                template: require('html-webpack-template'),
                appMountId: 'app',
                title: 'e-logs',
                favicon: "./public/images/favicon.ico",
                meta: [
                    {name: "viewport", content: "width=device-width,initial-scale=1.0"},
                    {name: "description", content: "The worlds best electronic journaling system"},
                    {name: "keywords", content: "journals, e-logs"},
                ],
                links: [

                    {rel: "manifest", href: "/manifest.json"},
                ],
                lang: 'en-US',
                bodyHtmlSnippet: "<noscript> Ваш браузер не поддерживает Javascript</noscript>",
                publicPath: (process.env.NODE_ENV === 'production') ? '/vueapp/' : undefined,
            }),
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
                            filename: path.resolve(__dirname, './e-logs-sw.js')
                        }
                    ],
                }
            ),
            new ResourceHintWebpackPlugin(),
        ],
    },

    baseUrl: (process.env.NODE_ENV === 'production') ? '/vueapp/' : undefined,
    outputDir: undefined,
    assetsDir: undefined,
    runtimeCompiler: true,
    productionSourceMap: undefined,
    parallel: undefined,
    css: undefined
};
