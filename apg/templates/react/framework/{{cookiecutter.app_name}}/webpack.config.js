const path = require('path');

module.exports = env => ({
  mode: (env && env.production) ? 'production' : 'development',
  entry: './src/index.jsx',
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, '{{cookiecutter.dist_relative_path}}')
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
});