import random
import time
import Utils.Utils as Utils


class TestSubsystem1(Utils.Subsystem):
    def __init__(self, ListofSubsystem: list[Utils.Subsystem]):
        super().__init__()
        self.ListofSubsystem = ListofSubsystem

    def getSubsystem(self, subsystemType):
        for subsystem in self.ListofSubsystem:
            if type(subsystem) is subsystemType:
                return subsystem

    def periodic(self):
        while True:
            try:
                pass

            except:
                print("FAIL!!!")
