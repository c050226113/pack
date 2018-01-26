import PackConf from "../../../pack.conf";

function get_new_file_path_dir(file_path){
    let tpl_path = file_path.replace(/\\/g, '/');
    let tpl_path_list = tpl_path.split('/');
    let index = tpl_path_list.indexOf(PackConf.root);
    let i;
    let arr1 = [];
    for(i=0;i<index;i++){
        arr1.push(tpl_path_list[i])
    }
    let arr2 = [];
    for(i=index+1;i<tpl_path_list.length;i++){
        arr2.push(tpl_path_list[i])
    }
    let new_path = arr1.concat([PackConf.root, PackConf.dist]).concat(arr2);
    new_path.pop();
    return new_path.join('/');
}

export default get_new_file_path_dir;

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
