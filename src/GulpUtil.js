"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var pack_conf_1 = require("../../../pack.conf");
var get_new_file_path_dir_1 = require("./get_new_file_path_dir");
var GulpUtil = (function () {
    function GulpUtil() {
    }
    GulpUtil.dec = function (func) {
        return function (json) {
            var old_file_path = typeof json === 'object' ? json['history'][0] : json;
            var new_path_dir = get_new_file_path_dir_1.default(old_file_path) + '/';
            console.log(old_file_path + " changed");
            func(old_file_path, {
                file_dir: new_path_dir,
                file_name: old_file_path.split('\\').pop(),
                upload_host: pack_conf_1.default.upload_host,
                upload_port: pack_conf_1.default.upload_port,
                upload_user: pack_conf_1.default.upload_user,
                upload_pwd: pack_conf_1.default.upload_pwd,
                upload_root: pack_conf_1.default.upload_root,
                root: pack_conf_1.default.root,
            });
        };
    };
    return GulpUtil;
}());
exports.default = GulpUtil;
;
//# sourceMappingURL=GulpUtil.js.map