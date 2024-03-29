var ws;
var msgbuf = "";


window.onload = function() {
  ws = new WebSocket("ws://"+hostname+":3000/ws");

  ws.onmessage = function(e) {
    dispatchMsg(e.data);
  };
}

function sendMsg() {
  ws.send(document.getElementById('msg').value  + "\r");
}

function echo() {
  ws.send("echo\r");
}

function soundSheep() {
    ws.send("s1\r");
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
    ws.send("{ \"component\": \"sound\", \"sound\": \"" + name + "\" }\r");
}
function startCam() {
    ws.send("{ \"component\": \"cam\", \"action\": \"start\" }\r");
}

function stopCam() {
    ws.send("{ \"component\": \"cam\", \"action\": \"stop\" }\r");
}
