const path = require('path');

module.exports = {
    entry: {
            main:'./src/main.js',
    },
    output: {
        path:path.resolve(__dirname,'../dist'),
        filename:'[name].js'
    },
    module: {
        rules: [
        {
            test: /\.css$/,
            use: [
                { loader: "style-loader"},
                {
                  loader: 'css-loader',
                  options: {
                      modules: true
                  }
                },
            ]
        }],
    },
};