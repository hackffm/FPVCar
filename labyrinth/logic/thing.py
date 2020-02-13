class Thing:

    def __init__(self, labyrinth, tid):
        self.labyrinth = labyrinth
        self.tid = tid

    def handleMessage(self, msg, m):
        print(msg)
