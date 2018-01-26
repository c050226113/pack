import * as Ws from "ws";


export default class StartServer{
    private socket;
    constructor (host, port){
        this.socket = new Ws(`ws://${host}:${port}`);
        this.socket.on('open', this.open);
        this.socket.on('message', this.message);
    }

    send(str){
        this.socket.send(str);
    }

    open(){

    }

    message(data){

    }
}