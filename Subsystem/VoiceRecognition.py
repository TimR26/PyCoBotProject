import string
import threading
import time
import Utils.Utils as Utils
import pyaudio
import wave
from faster_whisper import WhisperModel


class VoiceRecognition(Utils.Subsystem):
    model_size = "distil-large-v3"

    model = WhisperModel(model_size, device="cuda", num_workers=4, compute_type="int8")

    def __init__(self, ListofSubsystem: list[Utils.Subsystem]):
        super().__init__()
        self.ListofSubsystem = ListofSubsystem
        self.Text: list[str] = []
        # Audio settings
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

        # Global variables
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.recording = False

    def getSubsystem(self, subsystemType):
        for subsystem in self.ListofSubsystem:
            if type(subsystem) is subsystemType:
                return subsystem

    def periodic(self):
        while True:
            try:
                if self.recording:
                    self.frames = []
                    stream = self.audio.open(
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK,
        )
                    while self.recording:
                        data = stream.read(self.CHUNK)
                        self.frames.append(data)
                    stream.stop_stream()
                    stream.close()

                    wf = wave.open(self.WAVE_OUTPUT_FILENAME, "wb")
                    wf.setnchannels(self.CHANNELS)
                    wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                    wf.setframerate(self.RATE)
                    wf.writeframes(b"".join(self.frames))
                    threading.Thread(target=self.ProscessRecoding,args=(self.WAVE_OUTPUT_FILENAME,)).start()


            except:
                print("FAIL!!!")


    def startRecording(self, event=None):  # Add event=None
        self.recording = True

    def stopRecording(self, event=None):  # Add event=None
        self.recording = False

    # Function to stop recording and transcribe
    def ProscessRecoding(self, WAVE_OUTPUT_FILENAME):
        ct = time.process_time()
        segments, info = self.model.transcribe(
            WAVE_OUTPUT_FILENAME, language="en", beam_size=5
        )
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            self.Text.append(''.join(filter(lambda x: x not in string.punctuation, segment.text.lower())).strip())
            print(self.Text)
            print(time.process_time()-ct)
