const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const fs = require('fs');

const plugins = [
  new CleanWebpackPlugin(),
  new HtmlWebpackPlugin({
    template: './public/index.html'
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
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    publicPath: '/'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      }
    ]
  },
  plugins,
  devServer: {
    static: {
      directory: path.join(__dirname, 'dist')
    },
    host: '0.0.0.0',
    port: 8080,
    hot: true,
    historyApiFallback: true,
    allowedHosts: 'all',
    client: {
      webSocketURL: 'ws://localhost:8080/ws'
    }
  }
}; 