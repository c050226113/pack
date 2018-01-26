"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var pack_conf_1 = require("../../../pack.conf");
function get_new_file_path_dir(file_path) {
    var tpl_path = file_path.replace(/\\/g, '/');
    var tpl_path_list = tpl_path.split('/');
    var index = tpl_path_list.indexOf(pack_conf_1.default.root);
    var i;
    var arr1 = [];
    for (i = 0; i < index; i++) {
        arr1.push(tpl_path_list[i]);
    }
    var arr2 = [];
    for (i = index + 1; i < tpl_path_list.length; i++) {
        arr2.push(tpl_path_list[i]);
    }
    var new_path = arr1.concat([pack_conf_1.default.root, pack_conf_1.default.dist]).concat(arr2);
    new_path.pop();
    return new_path.join('/');
}
exports.default = get_new_file_path_dir;
// const http=require('http');
// const queryString=require('querystring');
// function http_curl(params){
//     let contents = '';
//     if(params){
//         contents  =  queryString.stringify(params);
//     }
//     //声明请求的参数 options
//     let options={
//         host:'127.0.0.1',
//         path:'/',
//         port:port,
//         method:'GET',
//         // headers:{
//         //     'Content-Type':'application/x-www-form-urlencoded',
//         //     'Content-Length':contents.length
//         // }
//     };
//     //开始发送请求
//     let req  =  http.request(options,(res)=>{
//         // res.setEncoding('utf-8');
//         // res.on('data',(data)=>{
//         //     console.log('return :');
//         //     console.log(data);
//         // });
//     });
//     req.on('error', function(e) {
//         // console.log('problem with request: ' + e.message);
//     });
//     req.write(contents);
//     req.end();
// }
//# sourceMappingURL=get_new_file_path_dir.js.map