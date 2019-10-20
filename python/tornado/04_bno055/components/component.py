class Component:

    def __init__(self):
        self.all = 'all'
        self.failed = 'failed'

    def handleMessage(self, message):
        print(message)
