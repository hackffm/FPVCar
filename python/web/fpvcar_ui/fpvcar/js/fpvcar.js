var configuration = {};
var debug = false;
var ws;
var msgbuf = "";
Number.prototype.map = function(in_min, in_max, out_min, out_max) {
  return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

window.onload = function() {
 /*
  ws = new WebSocket("ws://"+ip_first+":9090/websocket");

  ws.onmessage = function(e) {
    dispatchMsg(e.data);
  };
  ws.onopen = function (){
      ws.send("{ \"component\": \"config\", \"load\": \"configuration\" }\r")
  }
  */
  var canvas = document.getElementById("myCanvas");
  var ctx = canvas.getContext("2d");
  var rect = canvas.getBoundingClientRect();
  var mdown = false;
  var pos;
  var width = 640;
  var height = 480;
  canvas.addEventListener("mousedown", inputStart, false);
  canvas.addEventListener("mouseup", inputEnd, false);
  canvas.addEventListener("mouseout", function(e) {
    mdown = false;
  }, false);
  canvas.addEventListener('mousemove', inputMove, false);
  canvas.addEventListener("touchstart", inputStart, false);
  canvas.addEventListener("touchend", inputEnd, false);
  canvas.addEventListener("touchmove", inputMove, false);

  function inputStart() {
    mdown = true;
  }

  function inputEnd() {
    inputMove({
      clientX: Math.round(rect.width / 2 + rect.left),
      clientY: Math.round(rect.height / 2 + rect.top)
    });
    mdown = false;
  }

  function inputMove(e) {
    if (mdown) {
      if (e.touches && e.touches.length > 0) {
        pos = getMousePos(e.touches[0]);
      } else {
        pos = getMousePos(e);
      }

      centerPos(pos);
      //mapCenterPos(pos);
      toLeftRight(pos);
      printPos(pos);
      drawHandle(pos);
    }
  }

  function getMousePos(evt) {
    var pos = {
      x: Math.round(evt.clientX) - Math.round(rect.left),
      y: Math.round(evt.clientY) - Math.round(rect.top)
    };
    pos.ox = pos.x;
    pos.oy = pos.y;
    return pos;
  }

  function centerPos(pos) {
    pos.cx = pos.x - rect.width / 2;
    pos.cy = rect.height / 2 - pos.y;
  }

  function toLeftRight(pos) {
    pos.left = Math.min(pos.cy + pos.cx, width / 2);
    pos.right = Math.min(pos.cy - pos.cx, height / 2);
    return pos;
  }

  function mapCenterPos(pos) {
    pos.cx = Math.round(pos.cx.map(0, rect.width / 2, 0, width / 2));
    pos.cy = 254 - Math.round(pos.cy.map(0, rect.height / 2, 0, height / 2));
  }

  function printPos(pos) {
    document.getElementById("xy").innerHTML = "x:" + pos.x + "  y:" + pos.y;
    document.getElementById("cxcy").innerHTML = "cx:" + pos.cx + "  cy:" + pos.cy;
	if(pos.left > 255) pos.left = 255;
	if(pos.left < -255) pos.left = -255;
	if(pos.right > 255) pos.right = 255;
	if(pos.right < -255) pos.right = -255;
    document.getElementById("lr").innerHTML = "l:" + pos.left + "  r:" + pos.right;
  }

  function drawHandle(pos) {
    ctx.clearRect(0, 0, rect.width, rect.height);
    var s = 10;
    ctx.fillRect(pos.ox - s / 2, pos.oy - s / 2, s, s);

    ctx.beginPath();
    ctx.moveTo(rect.width / 2, rect.height / 2);
    ctx.lineTo(pos.ox, pos.oy);
    ctx.stroke();
  }

  document.getElementById("myCamera_start").addEventListener("click",function(){send_component_action("cam","start")});
  document.getElementById("myCamera_stop").addEventListener("click",function(){send_component_action("cam","stop")});
}

function dispatchMsg(msg) {
    if(msg.startsWith('V')) {
      var tokens = msg.split(':');
      document.getElementById('vbus').innerHTML = tokens[1];
      return
    }
    if(msg.startsWith('v')) {
      var tokens = msg.split(':');
      document.getElementById('vbat').innerHTML = tokens[1];
      document.gauges.get('myBattery').value = tokens[1];
      return
    }

    try {
      msg = JSON.parse(msg);
      if (msg.hasOwnProperty('sensor')) {
        _sensor = msg.sensor;
        if(_sensor.hasOwnProperty('temperature')){
            document.gauges.get('myTemperature').value = _sensor.temperature;
        }
        if(_sensor.hasOwnProperty('heading')){
            document.gauges.get('myCompass').value = _sensor.heading.toFixed(0);
        }
        return
      }
      if (msg.hasOwnProperty('config')){
        configuration = msg['config'];
        debug = configuration['debug']
        document.getElementById('Config_Hostname').value = configuration['name']
        return
      }
    } catch (e) {
      console.log(e)
    }
    document.getElementById('outputMessage').value = msg;
}

function echo() {
  ws.send("echo\r");
}

function fetchConfig() {
  ws.send("{ \"component\": \"config\", \"load\": \"all\" }\r")
}

function fetchStats() {
    ws.send("{ \"component\": \"stats\" }\r");
}
function send_component_action(c_name, c_action, ){
    ws.send("{ \"component\": \"" + c_name + "\", \"action\": \"" + c_action + "\" }\r");
}
function send_component_action_value(c_name, c_action_name, c_action_value){
    ws.send("{ \"component\": \"" + c_name + "\", \"" + c_action_name + "\": \"" + c_action_value + "\" }\r");
}
function sendMsg() {
  ws.send(document.getElementById('msg').value  + "\r");
}
