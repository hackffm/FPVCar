var table_sensor = document.getElementById("table_sensor");

function fetchSensor() {
    ws.send("{ \"component\": \"sensor\", \"sensor\": \"all\" }\r");
}

function fill_sensor_data(data) {
    var r = new Array(), j = -1;
    for (var k in data) {
        if (data.hasOwnProperty(k)) {
            r[++j] ='<tr><td>';
            r[++j] = k;
            r[++j] = '</td><td>';
            r[++j] = data[k];
            r[++j] = '</td></tr>';
        }
    }
    table_sensor.innerHTML = (r.join(''));
}
