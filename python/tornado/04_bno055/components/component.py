class Component:

    def __init__(self, ser='not needed'):
        self.all = 'all'
        self.failed = 'failed'
        self.ser = ser

    def handleMessage(self, message):
        print(message)
