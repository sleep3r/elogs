const webpack = require('webpack');
const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const BundleTracker = require('webpack-bundle-tracker');
const Cleaner = require('webpack-cleanup-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

const devMode = process.env.NODE_ENV !== 'production';

module.exports = {
    mode: 'development',
    entry: './src/main.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'public')
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: "babel-loader",
                        options: {
                            cacheDirectory: true,
                        }
                    }
                ],
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.css$/,
                use: [
                    // 'style-loader',
                    'vue-style-loader',
                    'css-loader',
                ],
            },
            {
                test: /\.scss$/,
                use: [
                    // 'style-loader',
                    'vue-style-loader',
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
                test: /\.(gif|png|jpe?g|svg|ico)$/i,
                loader: 'url-loader',
                // loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath: 'images/',
                    limit: 8192,
                },
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve(__dirname, "../src")
        }
    },
    plugins: [
        // Jquery loader plugin.
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            _: 'lodash',
            // Popper: ['popper.js', 'default'],
        }),
        new VueLoaderPlugin(),
        new webpack.HotModuleReplacementPlugin(),
        // new Cleaner(),
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
        })
    ],
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
