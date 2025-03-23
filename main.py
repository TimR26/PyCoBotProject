import threading
import time
from Utils import Subsystem
from TestSubsystem import TestSubsystem
from TestSubsystem1 import TestSubsystem1

if __name__ == "__main__":
    listOfSubsystems: list[Subsystem] = []
    ss = TestSubsystem(listOfSubsystems,1,"Test")
    tt = TestSubsystem1(listOfSubsystems, 2,"IDK")
    listOfSubsystems.append(ss)
    listOfSubsystems.append(tt)

    

    listOfThreads: list[threading.Thread] = []

    for subsystem in listOfSubsystems:
            t = threading.Thread(target=subsystem.periodic)
            listOfThreads.append(t)
            t.start()
            

    while True:
        pass