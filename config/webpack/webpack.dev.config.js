;const baseConfig = require('./webpack.base.config.js');

// Karma webpack config
module.exports = (opts) => {

    const config = baseConfig(opts);

    return {
        ...config,
        devtool: 'inline-source-map',
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
        },
    };
};
