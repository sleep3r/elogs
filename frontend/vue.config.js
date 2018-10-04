const fs = require('fs')
const webpack = require('webpack')

module.exports = {
    devServer: {
        open: process.platform === 'darwin',
        host: '127.0.0.1',
        port: 8080,
        https: {
            key: fs.readFileSync('../server.key'), // путь до твоего файла
            cert: fs.readFileSync('../server.crt'), // путь до твоего файла
            ca: fs.readFileSync('../Local Certificate.pem'), // путь до твоего файла
        },
        hotOnly: false,
    },
    configureWebpack: {
        module: {
            rules: [
                {
              test: /\.pdf$/,
              loader: 'file-loader',
            }
          ]
        },
        plugins: [
            new webpack.DefinePlugin({
                'process.env.NODE_ENV': JSON.stringify('production')
            })
        ]
    }
}