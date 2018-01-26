import PackConf from "../../../pack.conf";
import get_new_file_path_dir from "./get_new_file_path_dir";

export default class GulpUtil{
    static dec(func){
        return function(json){
            let old_file_path = typeof json === 'object' ? json['history'][0]:json;
            let new_path_dir = get_new_file_path_dir(old_file_path) + '/';
            console.log(`${old_file_path} changed`);
            func(old_file_path, {
                file_dir: new_path_dir,
                file_name: old_file_path.split('\\').pop(),
                upload_host: PackConf.upload_host,
                upload_port: PackConf.upload_port,
                upload_user: PackConf.upload_user,
                upload_pwd: PackConf.upload_pwd,
                upload_root: PackConf.upload_root,
                root: PackConf.root,
            });
        }
    }
};