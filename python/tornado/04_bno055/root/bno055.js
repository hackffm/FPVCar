document.getElementById("btm_bno055").addEventListener("click", function (ev) { fetchSensor() })
var table_sensor = document.getElementById("table_sensor");

function fetchSensor() {
    ws.send("{ \"component\": \"sensor\", \"sensor\": \"all\" }\r");
}

function fill_sensor_data(data){
     var r = new Array(), j = -1;
     for (var key=0, size=data.length; key<size; key++){
         r[++j] ='<tr><td>';
         r[++j] = data[key][0];
         r[++j] = '</td><td>';
         r[++j] = data[key][1];
         r[++j] = '</td></tr>';
     }
     table_sensor.html(r.join(''));
}