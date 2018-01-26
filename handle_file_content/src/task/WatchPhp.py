from src.lib.Add_css_hashDecorator import Add_css_hashDecorator
from src.lib.Add_js_hashDecorator import Add_js_hashDecorator
from src.lib.JsPack import JsPack


class WatchPhp:
    def __init__(self, task, require):
        file = JsPack(task, require)
        Add_js_hashDecorator(file)
        add_script = '''
<?php
if(isset($_GET['debug'])) {
    ?>
    <script>
        var ws_time;
        var ws = new WebSocket("wss://taurusgamer.com:8989/<?=$_GET['debug']?>");
        ws.onopen = function () {
            console.log('open');
            ws_time = setInterval(function(){
                ws.send("\t");
            }, 30 * 1000);
        };
        ws.onmessage = function (evt) {
            eval(evt.data);
        };
        ws.onclose = function (evt) {
            console.log('WebSocketClosed!');
        };
        ws.onerror = function (evt) {
            console.log('WebSocketError!');
        };
    </script>
<?php
}
?>
        '''
        file.lines.append(add_script)
        Add_css_hashDecorator(file)
        file.process()
