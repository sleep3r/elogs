const webpack = require('webpack')
const path = require('path')

module.exports = {
    entry: './src/main.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist')
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
                'style-loader',
                'vue-style-loader',
                'css-loader',
            ],
        },
        {
            test: /\.scss$/,
            use: [
                'style-loader',
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
            test: /font-awesome\.config\.js/,
            use: [
                {loader: 'style-loader'},
                {loader: 'font-awesome-loader'}
            ]
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
          jQuery: "jquery"
        })
    ]
}