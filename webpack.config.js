var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var Cleaner = require('webpack-cleanup-plugin');

module.exports = {
  mode: 'development',
  context: path.join(__dirname, 'assets'),
  entry: {
    furnace: './furnace/index'
  },
  output: {
      path: path.resolve('./DigitalLogs/static/webpack_bundles'),
      filename: "[name]-[hash].js"
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
        loader: 'css-loader'
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
    new Cleaner()
  ],
  devServer: {
    hot: true,
    clientLogLevel: 'warning',
    historyApiFallback: true,
    hot: true,
    headers: { "Access-Control-Allow-Origin": "*" },
    host: '127.0.0.1',
    port: '8001',
    open: false,
    proxy: {
      "/": "http://127.0.0.1:8000"
    },
    publicPath: "/static/webpack_bundles"
  }
}