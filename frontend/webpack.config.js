const path = require('path');
const webpack = require('webpack');

module.exports = (env, argv) => {
  const isDevelopment = argv.mode === 'development';
  const isProduction = argv.mode === 'production';

  return {
    entry: './src/main.ts',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: isDevelopment ? '[name].js' : '[name].[contenthash].js',
      chunkFilename: isDevelopment ? '[name].chunk.js' : '[name].[contenthash].chunk.js',
      clean: true,
      assetModuleFilename: 'assets/[hash][ext][query]'
    },
    devtool: isDevelopment ? 'source-map' : 'source-map',
    devServer: {
      port: 3000,
      hot: true,
      historyApiFallback: true,
      compress: true,
      client: {
        overlay: {
          errors: true,
          warnings: false
        }
      }
    },
    module: {
      rules: [
        {
          test: /\.ts$/,
          use: 'ts-loader',
          exclude: /node_modules/
        },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader'],
          type: 'javascript/auto'
        },
        {
          test: /\.(png|jpg|jpeg|gif|svg)$/,
          type: 'asset',
          parser: {
            dataUrlCondition: {
              maxSize: 8 * 1024
            }
          }
        }
      ]
    },
    resolve: {
      extensions: ['.ts', '.js', '.json'],
      alias: {
        '@': path.resolve(__dirname, 'src/')
      }
    },
    performance: {
      maxEntrypointSize: 300000,
      maxAssetSize: 300000,
      hints: isProduction ? 'error' : 'warning'
    },
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            priority: 10,
            reuseExistingChunk: true
          },
          chartjs: {
            test: /[\\/]node_modules[\\/]chart\.js/,
            name: 'chartjs',
            priority: 20,
            reuseExistingChunk: true
          }
        }
      },
      runtimeChunk: 'single',
      minimize: isProduction
    },
    plugins: [
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify(argv.mode),
        'process.env.API_BASE_URL': JSON.stringify(
          process.env.API_BASE_URL || 'http://localhost:8000'
        )
      }),
      ...(isProduction ? [
        new (require('webpack-bundle-analyzer').BundleAnalyzerPlugin)({
          analyzerMode: 'static',
          openAnalyzer: false,
          reportFilename: 'stats.html'
        })
      ] : [])
    ]
  };
};
