# taken from Adafruit BNO055 WebGL Example

import json
import threading
import time

from flask import *

import board
import busio
import adafruit_bno055
i2c = busio.I2C(board.SCL, board.SDA)

bno = adafruit_bno055.BNO055(i2c)
BNO_UPDATE_FREQUENCY_HZ = 10
CALIBRATION_FILE = 'calibration.json'

app = Flask(__name__)

bno_data = {}
bno_changed = threading.Condition()

bno_thread = None


def read_bno():
    """Function to read the BNO sensor and update the bno_data object with the
    latest BNO orientation, etc. state.  Must be run in its own thread because
    it will never return!
    """
    while True:
        # Capture the lock on the bno_changed condition so the bno_data shared
        # state can be updated.
        with bno_changed:
            bno_data['euler'] = bno.euler
            bno_data['temp'] = bno.temperature
            bno_data['quaternion'] = bno.quaternion
            bno_data['calibration'] = bno.calibration_status
            # Notify any waiting threads that the BNO state has been updated.
            bno_changed.notifyAll()
        # Sleep until the next reading.
        time.sleep(1.0/BNO_UPDATE_FREQUENCY_HZ)

def bno_sse():
    """Function to handle sending BNO055 sensor data to the client web browser
    using HTML5 server sent events (aka server push).  This is a generator function
    that flask will run in a thread and call to get new data that is pushed to
    the client web page.
    """
    # Loop forever waiting for a new BNO055 sensor reading and sending it to
    # the client.  Since this is a generator function the yield statement is
    # used to return a new result.
    while True:
        # Capture the bno_changed condition lock and then wait for it to notify
        # a new reading is available.
        with bno_changed:
            bno_changed.wait()
            # A new reading is available!  Grab the reading value and then give
            # up the lock.
            heading, roll, pitch = bno_data['euler']
            temp = bno_data['temp']
            x, y, z, w = bno_data['quaternion']
            sys, gyro, accel, mag = bno_data['calibration']
        # Send the data to the connected client in HTML5 server sent event format.
        data = {'heading': heading, 'roll': roll, 'pitch': pitch, 'temp': temp,
                'quatX': x, 'quatY': y, 'quatZ': z, 'quatW': w,
                'calSys': sys, 'calGyro': gyro, 'calAccel': accel, 'calMag': mag }
        yield 'data: {0}\n\n'.format(json.dumps(data))


@app.before_first_request
def start_bno_thread():
    global bno_thread
    # Kick off BNO055 reading thread.
    bno_thread = threading.Thread(target=read_bno)
    bno_thread.daemon = True  # Don't let the BNO reading thread block exiting.
    bno_thread.start()


@app.route('/bno')
def bno_path():
    return Response(bno_sse(), mimetype='text/event-stream')


@app.route('/load_calibration', methods=['POST'])
def load_calibration():
    # Load calibration from disk.
    #
    # TODO: implement this
    #
    return 'OK'


@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
