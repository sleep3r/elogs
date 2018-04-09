var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var Cleaner = require('webpack-cleanup-plugin');

module.exports = {
  mode: 'development',
  context: path.join(__dirname, 'assets'),
  entry: './index',
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
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new Cleaner()
  ]
}