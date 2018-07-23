const path = require('path');
let HtmlWebpackPlugin = require('html-webpack-plugin');//HTML打包
const uglify = require('uglifyjs-webpack-plugin');//压缩
const extractTextPlugin = require('extract-text-webpack-plugin');//CSS分离

module.exports = {
    mode:'development',
    entry: {
            start_js:'./src/index.js',
    },
    output: {
        path:path.resolve(__dirname,'../dist'),
        filename:'[name].js'
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: extractTextPlugin.extract({
                    fallback: "style-loader",
                    use: "css-loader"
                  }),
                  /*
                use: [
                    { loader: "style-loader"},
                    {
                      loader: 'css-loader',
                      options: {
                          modules: true
                      }
                    },
                ]*/
            },
            {
                test:/\.(png|jpg|gif|jpeg)/,  //是匹配图片文件后缀名称
                use:[{
                    loader:'url-loader', //是指定使用的loader和loader的配置参数
                    options:{
                        limit:8192  //是把小于500B的文件打成Base64的格式，写入JS
                    }
                }]
            },
            {
                test: /\.html$/,
                use:[{loader: 'html-withimg-loader'}]
            },
        ],
        /*//CSS无效写法一，无论是否exclude
        rules: [{
            test: /\.css$/,
            use: {
                loader: "style-loader",
                loader: "css-loader",
            }},
            //exclude: /node_modules/
        ],
        */
        /*//CSS无效写法二
        rules: [
            {test: /\.css$/, loader:ETP.extract("style-loader","css-loader") },//会出错、CSS无效
        ],
        */
    },
    devServer: {
        contentBase: path.resolve(__dirname,'../dist'),//本地服务器所加载的页面所在的目录
        host:'localhost',
        historyApiFallback: true,//不跳转
        inline: true,//实时刷新
        compress:true,
        port:8888
    },
    plugins: [
        // 通过new一下这个类来使用插件
        new HtmlWebpackPlugin({
            // 指定一个html文件作为模板
            template: path.resolve(__dirname,'../src/index.html'),
            hash: true, // 会在打包好的bundle.js后面加上hash串
        }),
        new uglify(),
        new extractTextPlugin("css/index.css")  //这里的/css/index.css 是分离后的路径
    ]
};