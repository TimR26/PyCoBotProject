import threading
import Gui
from Utils.Utils import Subsystem
from Subsystem.Vision import Vision
import tkinter as tk


if __name__ == "__main__":
    listOfSubsystems: list[Subsystem] = []
    ss = Vision(listOfSubsystems)
    listOfSubsystems.append(ss)
    listOfThreads: list[threading.Thread] = []

    for subsystem in listOfSubsystems:
            t = threading.Thread(target=subsystem.periodic)
            listOfThreads.append(t)
            t.start()

    gui: Gui.Gui = Gui.Gui(listOfSubsystems)
    gui.start()
            

    