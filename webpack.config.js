const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const Cleaner = require('webpack-cleanup-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const CompressionPlugin = require("compression-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const OfflinePlugin = require('offline-plugin');
const PurgecssPlugin = require('purgecss-webpack-plugin');


const devMode = process.env.NODE_ENV !== 'production';
module.exports = {
    mode: 'development',
    context: path.join(__dirname, 'assets'),
    entry: {
        messages: './notifications/index',
        leaching: './leaching/index',
        furnace: './furnace/index',
        index: './js/index',
        "index.min": './js/index',
    },
    output: {
        path: path.resolve('./static/webpack_bundles'),
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
            new OptimizeCSSAssetsPlugin({})
        ],
        splitChunks: {
            cacheGroups: {
                styles: {
                    name: 'styles',
                    test: /\.css$/,
                    chunks: 'all',
                    enforce: true
                }
            }
        }
    },
    module:
        {
            rules: [
                {
                    test: /\.js$/,
                    loader: 'babel-loader',
                    exclude: /node_modules/,
                    query: {compact: true},
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
                        // MiniCssExtractPlugin.loader,
                        'css-loader',
                    ],
                },
                {
                    test: /\.scss$/,
                    use: [
                        // 'style-loader',
                        'vue-style-loader',
                        // MiniCssExtractPlugin.loader,
                        'css-loader',
                        'sass-loader',
                    ],
                },
                {
                    test: /.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: 'fonts/'
                    }
                }
            ]
        }
    ,
    resolve: {
        alias: {
            'vue$':
                'vue/dist/vue.esm.js'
        }
    }
    ,
    plugins: [
        new webpack.ProvidePlugin({
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            $: 'jquery',
            moment: 'moment',
            Vue: ['vue/dist/vue.esm.js', 'default'],
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
        new CompressionPlugin(),
        new webpack.DefinePlugin({PRODUCTION: JSON.stringify(false)}),
        new MiniCssExtractPlugin({
            filename: "[name].css",
            chunkFilename: "[id].css"
        }),
        new webpack.SourceMapDevToolPlugin({
            test: '\\.((js)|(scc)|(scss))$',
            filename: '[name].js.map',
            exclude: /node_modules/,
        }),
        new OfflinePlugin(),
    ],
    devtool:
        false, //'inline-source-map',
    devServer:
        {
            hot: true,
            clientLogLevel:
                'warning',
            historyApiFallback:
                true,
            headers:
                {
                    "Access-Control-Allow-Origin":
                        "*"
                }
            ,
            host: '127.0.0.1',
            port:
                '8001',
            open:
                false,
            proxy:
                {
                    "/":
                        "http://127.0.0.1:8000"
                }
            ,
            publicPath: "/static/webpack_bundles"
        }
}
;
