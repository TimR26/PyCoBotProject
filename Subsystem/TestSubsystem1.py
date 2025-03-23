import random
import time
from Subsystem.TestSubsystem import TestSubsystem
import Utils.Utils as Utils

class TestSubsystem1(Utils.Subsystem):
    def __init__(self, ListofSubsystem: list[Utils.Subsystem], number: int, string: str):
        super().__init__()
        self.ListofSubsystem = ListofSubsystem
        self.number = number
        self.string = string

    def getSubsystem(self, subsystemType):
        for subsystem in self.ListofSubsystem:
            if type(subsystem) is subsystemType:
                return subsystem

    def periodic(self):
        ts0: TestSubsystem = self.getSubsystem(TestSubsystem)

        current = time.process_time()
        r = random.random()*5
        
        while True:
            try:
                if time.process_time()-current > r:
                    ts0.count()
                    current = time.process_time()
                    r = random.random()*5

                
                # time.sleep(10)
                # self.printE()
            except:
                print("FAIL!!!")
        
    
    def printE(self):
        print(self.string)