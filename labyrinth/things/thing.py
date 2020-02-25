class Thing:

    def __init__(self, labyrinth, tid):
        self.labyrinth = labyrinth
        self.tid = tid
        self.ser = None

    def handleMessage(self, msg, m):
        print(msg)
