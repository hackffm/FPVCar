import sys

from time import sleep


from multiprocessing import Process

from components import Base
from handlers import handler_default
from webserver import WebServer

components = {
    "base": Base(handler_default)
}

if __name__ == '__main__':

    debug = True
    running = True
    try:
        # start processes
        p1 = Process(target=WebServer, args=(components, debug))
        p1.daemon = True
        p1.start()

        print('PID Webserver', p1.pid)

        while running:
            sleep(0.5)
    except KeyboardInterrupt:
        print('ending with keyboard interrupt')
        running = False
        p1.terminate()
    except Exception as e:
        print('error in fpvcar __main__ ' + str(e))

    running = False
    print('[FPVCAR]bye')
    sys.exit()
