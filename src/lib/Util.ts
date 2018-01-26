import ChildProcess from "./ChildProcess";

export default class Util{
    static killProcessByPort(host=null, port=null, func=null){
        let line, lineList;
        host = host || '127.0.0.1';
        port = port || 9000;
        new ChildProcess(`netstat -ano`).exec((err, stdout , stderr ) => {
            if (stderr) console.log(stderr);
            let _break = false;
            for(line of stdout.split("\r\n")){
                lineList = line.trim().replace(/\s+/g," ").split(" ");
                if(lineList[0]==="TCP" && lineList[1] === `${host}:${port}`) {
                    let pid = lineList[4];
                    new ChildProcess(`tasklist`).exec((err, stdout, stderr) => {
                        if (stderr) console.log(stderr);
                        for (line of stdout.split("\r\n")) {
                            lineList = line.trim().replace(/\s+/g, " ").split(" ");
                            if (lineList[1] === pid) {
                                new ChildProcess(`taskkill -f -t -im ${lineList[0]}`).exec(() => {
                                    if (func)
                                        func()
                                })
                            }
                        }
                    });
                    _break = true;
                    break;
                }
            }
            if (!_break){
                if (func)
                    func()
            }
        });
    }
    static object_key_arr(obj){
        let arr = [];
        let key;
        for (key in obj){
            if (obj.hasOwnProperty(key)){
                arr.push(key)
            }
        }
        return arr;
    }
    static inEach(obj, func) {
        let ret,key;
        for (key in obj){
            if(obj.hasOwnProperty(key)){
                ret = func.call(this, obj[key], key);//回调函数
                if (ret === false) break;
            }
        }
    }

    // .pipe(htmlmin({
//     removeComments: true,//清除HTML注释
//     collapseWhitespace: true,//压缩HTML
//     collapseBooleanAttributes: true,//省略布尔属性的值 <input checked="true"/> ==> <input />
//     removeEmptyAttributes: true,//删除所有空格作属性值 <input id="" /> ==> <input />
//     removeScriptTypeAttributes: true,//删除<script>的type="text/javascript"
//     removeStyleLinkTypeAttributes: true,//删除<style>和<link>的type="text/css"
//     minifyJS: true,//压缩页面JS
//     minifyCSS: true//压缩页面CSS
// }))
}