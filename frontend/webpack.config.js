const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const fs = require('fs');

const plugins = [
  new CleanWebpackPlugin(),
  new HtmlWebpackPlugin({
    template: './public/index.html',
    inject: 'body'
  })
];

// Only add CopyWebpackPlugin if assets directory exists and has files
const assetsPath = path.join(__dirname, 'public/assets');
if (fs.existsSync(assetsPath) && fs.readdirSync(assetsPath).length > 0) {
  plugins.push(
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'public/assets',
          to: 'assets'
        }
      ]
    })
  );
}

module.exports = {
  entry: './src/index.ts',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: ['.ts', '.js']
  },
  plugins,
  devServer: {
    static: {
      directory: path.join(__dirname, 'dist'),
      publicPath: '/'
    },
    compress: true,
    port: 8080,
    hot: true,
    historyApiFallback: true
  },
  devtool: 'source-map'
}; 