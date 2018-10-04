module.exports = {
  configureWebpack: {
    module: {
    	rules: [
    		{
          test: /\.pdf$/,
          loader: 'file-loader',
        }
      ]
    }
  }
}