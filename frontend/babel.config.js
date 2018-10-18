module.exports = {
  presets: [
    '@vue/app'
  ],
  env: {
    'production': {
      'presets': ['minify']
    }
  },
  plugins: ['syntax-dynamic-import'],
  compact: true
}
