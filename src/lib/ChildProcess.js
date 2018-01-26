"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// import * as child_process from 'child_process';
var child_process = require("child_process");
var ChildProcess = (function () {
    function ChildProcess(cmd) {
        if (cmd === void 0) { cmd = null; }
        if (cmd) {
            this.cmd = cmd;
        }
        this.func = function (data) {
            console.log(data);
        };
    }
    ChildProcess.prototype.spawn = function (stdOut, stdErr, close) {
        if (stdOut === void 0) { stdOut = this.func; }
        if (stdErr === void 0) { stdErr = this.func; }
        if (close === void 0) { close = this.func; }
        var cmd_arr = this.cmd.split(' ');
        var file = cmd_arr.shift();
        var cmd = child_process.spawn(file, cmd_arr);
        cmd.stdout.on('data', function (data) {
            stdOut(data);
        });
        cmd.stderr.on('data', function (data) {
            stdErr('error:' + data);
        });
        cmd.on('close', function (code) {
            close('code:' + code);
        });
    };
    ChildProcess.prototype.exec = function (func) {
        if (func === void 0) { func = this.func; }
        child_process.exec(this.cmd, func);
    };
    return ChildProcess;
}());
exports.default = ChildProcess;
//# sourceMappingURL=ChildProcess.js.map