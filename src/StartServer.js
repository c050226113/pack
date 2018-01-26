"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Ws = require("ws");
var StartServer = (function () {
    function StartServer(host, port) {
        this.socket = new Ws("ws://" + host + ":" + port);
        this.socket.on('open', this.open);
        this.socket.on('message', this.message);
    }
    StartServer.prototype.send = function (str) {
        this.socket.send(str);
    };
    StartServer.prototype.open = function () {
    };
    StartServer.prototype.message = function (data) {
    };
    return StartServer;
}());
exports.default = StartServer;
//# sourceMappingURL=StartServer.js.map