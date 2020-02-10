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
    ws.send('{ "component": "self", "name": "controller '+urlVars.nbr+'", "type":"controller", "nbr":'+urlVars.nbr+' }');
  }
  ws.onmessage = function(e) {
    dispatchMsg(e.data);
  };
}

function dispatchMsg(msg) {
    console.log(msg);
    var tokens = msg.split(':');
    if(msg.startsWith('V')) {
        document.getElementById('vbus').innerHTML = tokens[1];
    } else
    if(msg.startsWith('v')) {
        document.getElementById('vbat').innerHTML = tokens[1];
    } else {
        //document.getElementById('out').value += msg;
    }
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
    ws.send('{ "entity": "labyrinth", "component": "showmessage", "text": "start"}\r');
}