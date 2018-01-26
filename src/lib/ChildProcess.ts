// import * as child_process from 'child_process';
import * as child_process from 'child_process';

export default class ChildProcess{
    private cmd:string;
    private func;

    constructor(cmd=null){
        if (cmd){
            this.cmd = cmd;
        }
        this.func = (data)=>{
            console.log(data)
        };
    }

    spawn(stdOut=this.func, stdErr=this.func, close=this.func){
        let cmd_arr = this.cmd.split(' ');
        let file = cmd_arr.shift();
        let cmd = child_process.spawn(file, cmd_arr);
        cmd.stdout.on('data', (data) => {
            stdOut(data);
        });
        cmd.stderr.on('data', (data) => {
            stdErr('error:'+data);
        });
        cmd.on('close', (code) => {
            close('code:'+code);
        });
    }

    exec(func=this.func){
        child_process.exec( this.cmd , func);
    }
}