const webpack = require('webpack'); 
const fs = require('fs');
const path = require('path');
// replace accordingly './.env' with the path of your .env file 
require('dotenv').config({ path: '../.env' }); 

function checkForCertificates() {
  const keyPath = path.resolve(__dirname, './privkey.pem');
  const certPath = path.resolve(__dirname, './fullchain.pem');

  return fs.existsSync(keyPath) && fs.existsSync(certPath);
}

module.exports = {
  mode: 'development', // change to production
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.(jsx|js)$/,
        include: path.resolve(__dirname, 'src'),
        exclude: /node_modules/,
        use: [{
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                "targets": "defaults" 
              }],
              '@babel/preset-react'
            ]
          }
        }]
      },
      {
        test: /\.s(a|c)ss$/,
        use: [
            'style-loader',
            'css-loader',
            'sass-loader'
        ],
      },
      {
        test: /\.png$/,
        use: [
            'file-loader'
        ],
      }
    ]
  },
  resolve: {
    modules: ['client', 'node_modules']
  },
  plugins: [
    new webpack.DefinePlugin({
      // Only giving it what it needs
      "process.env": {
        "SERVER_PORT": JSON.stringify(process.env.SERVER_PORT),
        "SERVER_URL": JSON.stringify(process.env.SERVER_URL),
        "CLIENT_PORT": JSON.stringify(process.env.CLIENT_PORT)
      }
    }),
  ],
  devServer: {
    client: {
      reconnect: true,
    },
    port: process.env.CLIENT_PORT, 
    allowedHosts: 'all',
    https: checkForCertificates() ? { // Use HTTPS conditionally
      key: fs.readFileSync(path.resolve(__dirname, './privkey.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, './fullchain.pem')),
    } : false, // Disable HTTPS if certificates are missing
  }
};
