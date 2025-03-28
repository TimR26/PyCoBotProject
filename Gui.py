
import tkinter as tk
from Utils import Utils
import Subsystem.Vision
import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image, ImageTk

class Gui():

    def __init__(self, ListofSubsystem: list[Utils.Subsystem]):
        self.ListofSubsystem = ListofSubsystem
        self.visionSubsystem: Subsystem.Vision.Vision = self.getSubsystem(Subsystem.Vision.Vision)
        self.currentFrame = self.visionSubsystem.get_new_colorFrame()
        
        # GUI Stuff
        self.root = tk.Tk()
        self.root.title("PyCobot")

        self.video_panel = tk.Label(self.root)
        self.video_panel.grid(column=1,row=0)
        self.video_panel.bind("<Button-1>", self.on_mouse_click)

        control_frame = tk.LabelFrame(self.root, text="Controls")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.SetOrigin = tk.Button(control_frame, text="SetOrigin", font=("Arial", 14),height=1,width=8,bg="lightgray", command=self.onButtonOriginPressed)
        self.SetOrigin.pack(padx=5, pady=5)

        self.SetLength = tk.Button(control_frame, text="SetLength", font=("Arial", 14),height=1,width=8,bg="lightgray", command=self.onButtonLengthPressed)
        self.SetLength.pack(padx=5, pady=5)

        self.SetWidth = tk.Button(control_frame, text="SetWidth", font=("Arial", 14),height=1,width=8,bg="lightgray", command=self.onButtonWidthPressed)
        self.SetWidth.pack(padx=5, pady=5)

        self.selected = 0

        self.periodic()

    def getSubsystem(self, subsystemType):
        for subsystem in self.ListofSubsystem:
            if type(subsystem) is subsystemType:
                return subsystem
            
    def getImage(self):
        self.currentFrame = self.visionSubsystem.get_new_colorFrame()

    def processImage(self):
        color_image = np.asanyarray(self.currentFrame.get_data())
        # Convert to PhotoImage
        img = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return ImageTk.PhotoImage(image=img)

    def periodic(self):

        if(self.selected == 1):
            self.SetOrigin.config(bg="lightgreen")
        else:
            self.SetOrigin.config(bg="lightgray")

        if(self.selected == 2):
            self.SetLength.config(bg="lightgreen")
        else:
            self.SetLength.config(bg="lightgray")

        if(self.selected == 3):
            self.SetWidth.config(bg="lightgreen")
        else:
            self.SetWidth.config(bg="lightgray")


        self.getImage()
        if self.currentFrame != None:
            imgtk = self.processImage()
            # Update panel
            self.video_panel.imgtk = imgtk
            self.video_panel.configure(image=imgtk)
        self.root.after(20, self.periodic)


    def start(self):
        self.root.mainloop()

    def on_mouse_click(self, event):
        currentFrame = self.currentFrame
        x, y = event.x, event.y
        point = self.visionSubsystem.pixel_to_point(currentFrame,x,y)
        print(point)

    def onButtonOriginPressed(self): 
        if self.selected == 1:
            self.selected = 0
        else:
            self.selected = 1

    def onButtonLengthPressed(self): 
        if self.selected == 2:
            self.selected = 0
        else:
            self.selected = 2

    def onButtonWidthPressed(self): 
        if self.selected == 3:
            self.selected = 0
        else:
            self.selected = 3
        