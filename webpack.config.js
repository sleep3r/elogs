const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const Cleaner = require('webpack-cleanup-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const HtmlMinifierPlugin = require('html-minifier-webpack-plugin');
// const CompressionPlugin = require("compression-webpack-plugin");
// const OfflinePlugin = require('offline-plugin');

const OPTIONS = {
    PROJECT_ROOT: __dirname,
    NODE_ENV: process.env.NODE_ENV,
    DEV_MODE: process.env.DEBUG !== 'True',
};

const devMode = process.env.NODE_ENV !== 'production';

let cacheObj = {};

module.exports = {
    target: "web",
    cache: cacheObj,
    mode: 'development',
    context: path.resolve(__dirname, 'assets'),
    entry: {
        index: './js/index',
        "index.min": './js/index',
        messages: './messages/index',
        furnace: './furnace/index',
        tables: './tables/index',
        vendor: [
            "jquery",
            "moment",
            "fullcalendar",
            // "webpack-material-design-icons",
            // 'font-awesome/scss/font-awesome.scss',
            'tether',
            // "font-awesome-webpack!./path/to/font-awesome.config.js",
        ],
    },
    output: {
        path: path.resolve(__dirname, 'static/webpack_bundles'),
        filename: "[name].js"
    },
    optimization: {
        minimizer: [
            new UglifyJsPlugin({
                include: /\.min\.js$/,
                cache: true,
                parallel: true,
                extractComments: true
            }),
            new OptimizeCSSAssetsPlugin({
                assetNameRegExp: /\.min\.css$/g,
                cssProcessor: require('cssnano'),
                cssProcessorOptions: {discardComments: {removeAll: true}},
                canPrint: true
            }),
        ],
    },
    module: {
        rules: [
            {
                test: /\.js?$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: "babel-loader",
                        options: {
                            cacheDirectory: true,
                        }
                    }
                    // "eslint-loader",
                    // 'jshint-loader',
                ],
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.html$/,
                loaders: ['file-loader?name=[name].html', 'extract-loader', 'html-loader']
            },
            {
                test: /\.css$/,
                use: [
                    // 'style-loader',
                    // 'vue-style-loader',
                    MiniCssExtractPlugin.loader,
                    // devMode ? 'vue-style-loader' : MiniCssExtractPlugin.loader,
                    'css-loader',
                ],
            },
            {
                test: /\.scss$/,
                use: [
                    // 'style-loader',
                    // 'vue-style-loader',
                    MiniCssExtractPlugin.loader,  //production shit
                    // devMode ? 'vue-style-loader' : MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader',
                ],
            },
            {
                test: /\.(jpe?g|png|gif|eot|ttf|svg|woff(2)?)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath: 'fonts/',
                },
            },
            {
                test: /bootstrap\/dist\/js\/umd\//, use: 'imports-loader?jQuery=jquery'
            },
            {
                test: /font-awesome\.config\.js/,
                use: [
                    {loader: 'style-loader'},
                    {loader: 'font-awesome-loader'}
                ]
            },
            {
                test: /\.(gif|png|jpe?g|svg|ico)$/i,
                // loader: 'url-loader',
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath: 'images/',
                    limit: 8192,
                },
            },
            {
                test: /\.pug$/,
                loader: 'pug-plain-loader'
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            'waypoints': 'waypoints/lib/jquery.waypoints.js'
        }
    },
    plugins: [
        new webpack.ProvidePlugin({
            moment: 'moment',
            Vue: ['vue/dist/vue.esm.js', 'default'],
            $: 'jquery',
            _: 'lodash',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            tether: 'tether',
            Tether: 'tether',
            'window.Tether': 'tether',
            Popper: ['popper.js', 'default'],
            Alert: 'exports-loader?Alert!bootstrap/js/dist/alert',
            Button: 'exports-loader?Button!bootstrap/js/dist/button',
            Carousel: 'exports-loader?Carousel!bootstrap/js/dist/carousel',
            Collapse: 'exports-loader?Collapse!bootstrap/js/dist/collapse',
            Dropdown: 'exports-loader?Dropdown!bootstrap/js/dist/dropdown',
            Modal: 'exports-loader?Modal!bootstrap/js/dist/modal',
            Popover: 'exports-loader?Popover!bootstrap/js/dist/popover',
            Scrollspy: 'exports-loader?Scrollspy!bootstrap/js/dist/scrollspy',
            Tab: 'exports-loader?Tab!bootstrap/js/dist/tab',
            Tooltip: "exports-loader?Tooltip!bootstrap/js/dist/tooltip",
            Util: 'exports-loader?Util!bootstrap/js/dist/util'
        }),
        new webpack.HotModuleReplacementPlugin(),
        new BundleTracker({filename: './webpack-stats.json'}),
        new Cleaner(),
        new HtmlWebpackPlugin(),
        new VueLoaderPlugin(),
        new UglifyJsPlugin({
            include: /\.min\.js$/, cache: true, parallel: true,
            extractComments: true, sourceMap: true
        }),
        new webpack.DefinePlugin({PRODUCTION: JSON.stringify(false)}),
        new MiniCssExtractPlugin({
            filename: devMode ? '[name].css' : '[name].[hash].css',
            chunkFilename: devMode ? '[id].css' : '[id].[hash].css',
        }),
        new OptimizeCSSAssetsPlugin({
            assetNameRegExp: /\.optimize\.css$/g,
            cssProcessor: require('cssnano'),
            cssProcessorPluginOptions: {
                preset: ['default', {discardComments: {removeAll: true}}],
            },
            canPrint: true
        }),
        new HtmlMinifierPlugin({
            // HTMLMinifier options
        })
        // new CompressionPlugin(),
        // new webpack.SourceMapDevToolPlugin({
        //     test: '\\.((js)|(scc)|(scss))$',
        //     filename: '[name].js.map',
        //     exclude: /node_modules/,
        // }),
        // new OfflinePlugin(),
    ],
    // devtool: "source-map",
    // devtool: false,
    devtool: "inline-source-map",
    devServer: {
        hot: true,
        clientLogLevel: 'warning',
        historyApiFallback: true,
        headers: {"Access-Control-Allow-Origin": "*"},
        host: '127.0.0.1',
        port: '8001',
        open: false,
        proxy: {"/": "http://127.0.0.1:8000"},
        publicPath: "/static/webpack_bundles"
    }
};
