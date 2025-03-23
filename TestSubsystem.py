import time
import Utils

class TestSubsystem(Utils.Subsystem):
    def __init__(self, ListofSubsystem: list[Utils.Subsystem], number: int, string: str):
        super().__init__()
        self.ListofSubsystem = ListofSubsystem
        self.number = number
        self.string = string

    def getSubsystem(self, subsystemType):
        for subsystem in self.ListofSubsystem:
            if type(subsystem) == subsystemType:
                return subsystem

    def periodic(self):
        num = self.number
        while True:
            try:
                if self.number != num:
                    self.printE()
                    num = self.number
                
            except:
                print("FAIL!!!")


    def count(self):
        self.number = self.number + 1

    
    def printE(self):
        print(self.number)