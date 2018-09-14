;const path = require('path');
const webpack = require('webpack');
const baseConfig = require('./webpack.base.config.js');

const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");


module.exports = (opts) => {

    return {
        ...config,
        devtool: "source-map",
        plugins: [
            ...config.plugins,
            // pass options to uglify
            new webpack.LoaderOptionsPlugin({
                minimize: true,
                debug: false,
            }),
            new UglifyJsPlugin({
                include: /\.min\.js$/,
                cache: true,
                parallel: true,
                extractComments: false,
                sourceMap: false,
                compress: {
                    warnings: false,
                },
                output: {
                    comments: false,
                },
            }),
            // removes duplicate modules
            new MiniCssExtractPlugin({
                filename: "[name].css",
                chunkFilename: "[id].css"
            }),

        ],
    };
};
