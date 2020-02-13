var ws;
var msgbuf = "";

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

window.onload = function() {
  urlVars = getUrlVars();
  msgPrefixCar = '{ "entity":"car", "nbr":"'+urlVars.nbr+'", "component":'
  ws = new WebSocket("ws://"+hostname+":3000/ws");
  ws.onopen = function(e) {
    ws.send('{ "thing": "ctrl1", "init":"true" }');
  }
  ws.onmessage = function(e) {
    dispatchMsg(e.data);
  };
}

function dispatchMsg(message) {
    console.log(message);
    if(!message.startsWith("{")) return;

    var msg = JSON.parse(message)
    if(msg.component == 'items') {
        if(msg.action == 'add') {
            addItem(msg)
        } else
        if(msg.action == 'rem') {
            remItem(msg)
        }
    }
}
function addItem(msg) {
    $("#items").append('<li id="'+msg.item+'" style="color:white;"><i class="fa-li fa fa-key" ></i>'+msg.item+'</li>');
}
function remItem(msg) {
    $('#'+msg.item).remove();
}


function updateStats(msg) {
    console.log(msg);
}
function playSound(name) {
    ws.send(msgPrefixCar + '"sound", "sound":"' + name + '" }\r');
}
function startCam() {
    ws.send('{ "component": "cam", "action": "start" }\r');
}
function startGame() {
    ws.send('{ "thing": "ctrl1", "component": "showmessage", "text": "start"}\r');
}
function rfid(id, from, action) {
    ws.send('{ "thing":"rfid", "id":"'+id+'", "car":"'+from+'", "action":"'+action+'" }\r');
}
function move(id, l, r) {
    ws.send('{ "thing":"'+id+'", "component":"base", "left":'+l+', "right":'+r+' }\r');
}