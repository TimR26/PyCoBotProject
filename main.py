import threading
from Utils.Utils import Subsystem
from Subsystem.VoiceRecognition import VoiceRecognition
import tkinter as tk
from Subsystem.TestSubsystem1 import TestSubsystem1

if __name__ == "__main__":
    listOfSubsystems: list[Subsystem] = []
    voiceRecognition = VoiceRecognition(listOfSubsystems)
    tt = TestSubsystem1(listOfSubsystems)
    listOfSubsystems.append(voiceRecognition)
    listOfSubsystems.append(tt)

    listOfThreads: list[threading.Thread] = []

    for subsystem in listOfSubsystems:
        t = threading.Thread(target=subsystem.periodic)
        listOfThreads.append(t)
        t.start()

    # GUI Stuff
    root = tk.Tk()
    root.title("Voice Transcription")

    record_button = tk.Button(root, text="Hold to Speak", font=("Arial", 14), width=20)
    record_button.pack(pady=20)

    transcription_label = tk.Label(
        root,
        text="Transcription will appear here.",
        font=("Arial", 12),
        wraplength=400,
        justify="left",
    )
    transcription_label.pack(pady=10)

    # Bind button press and release
    record_button.bind(
        "<ButtonPress>", voiceRecognition.startRecording
    )
    record_button.bind(
        "<ButtonRelease>", voiceRecognition.stopRecording
    )

    # Run GUI
    root.mainloop()
