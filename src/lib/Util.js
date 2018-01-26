"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var ChildProcess_1 = require("./ChildProcess");
var Util = (function () {
    function Util() {
    }
    Util.killProcessByPort = function (host, port, func) {
        if (host === void 0) { host = null; }
        if (port === void 0) { port = null; }
        if (func === void 0) { func = null; }
        var line, lineList;
        host = host || '127.0.0.1';
        port = port || 9000;
        new ChildProcess_1.default("netstat -ano").exec(function (err, stdout, stderr) {
            if (stderr)
                console.log(stderr);
            var _break = false;
            var _loop_1 = function () {
                lineList = line.trim().replace(/\s+/g, " ").split(" ");
                if (lineList[0] === "TCP" && lineList[1] === host + ":" + port) {
                    var pid_1 = lineList[4];
                    new ChildProcess_1.default("tasklist").exec(function (err, stdout, stderr) {
                        if (stderr)
                            console.log(stderr);
                        for (var _i = 0, _a = stdout.split("\r\n"); _i < _a.length; _i++) {
                            line = _a[_i];
                            lineList = line.trim().replace(/\s+/g, " ").split(" ");
                            if (lineList[1] === pid_1) {
                                new ChildProcess_1.default("taskkill -f -t -im " + lineList[0]).exec(function () {
                                    if (func)
                                        func();
                                });
                            }
                        }
                    });
                    _break = true;
                    return "break";
                }
            };
            for (var _i = 0, _a = stdout.split("\r\n"); _i < _a.length; _i++) {
                line = _a[_i];
                var state_1 = _loop_1();
                if (state_1 === "break")
                    break;
            }
            if (!_break) {
                if (func)
                    func();
            }
        });
    };
    Util.object_key_arr = function (obj) {
        var arr = [];
        var key;
        for (key in obj) {
            if (obj.hasOwnProperty(key)) {
                arr.push(key);
            }
        }
        return arr;
    };
    Util.inEach = function (obj, func) {
        var ret, key;
        for (key in obj) {
            if (obj.hasOwnProperty(key)) {
                ret = func.call(this, obj[key], key); //回调函数
                if (ret === false)
                    break;
            }
        }
    };
    return Util;
}());
exports.default = Util;
//# sourceMappingURL=Util.js.map