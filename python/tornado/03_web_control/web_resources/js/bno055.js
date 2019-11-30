var table_bno055 = document.getElementById("tblbno055");


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
    table_bno055.innerHTML = (r.join(''));
    document.getElementById("lblcompass").innerHTML = data.heading.toFixed(0);
}
