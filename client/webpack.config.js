const webpack = require('webpack'); 

// replace accordingly './.env' with the path of your .env file 
require('dotenv').config({ path: '../.env' }); 

const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  plugins: [
    new webpack.DefinePlugin({
      // Only giving it what it needs
      "process.env": {
        "SERVER_PORT": process.env.SERVER_PORT,
        "SERVER_URL": process.env.SERVER_URL
      }
    }),
  ]
};