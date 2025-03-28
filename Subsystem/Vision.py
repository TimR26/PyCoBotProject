import time

import numpy as np
import Utils.Utils as Utils
import pyrealsense2 as rs

class Vision(Utils.Subsystem):
    def __init__(self, ListofSubsystem: list[Utils.Subsystem]):
        super().__init__()
        self.ListofSubsystem = ListofSubsystem

        isRunning = False

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.profile = self.pipeline.start(self.config)
        self.depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()

        self.frames = []

        # np.


        


    def getSubsystem(self, subsystemType):
        for subsystem in self.ListofSubsystem:
            if type(subsystem) is subsystemType:
                return subsystem

    def periodic(self):
        current = time.time_ns()*(1/1000000.0)
        while True:
                frames = self.pipeline.wait_for_frames()
                self.frames.append(frames)
                for frame in self.frames:
                    if (time.time_ns()*(1/1000000.0))- frame.get_timestamp() >500:
                        self.frames.remove(frame)

    def get_new_colorFrame(self):
        try:
            return self.frames[len(self.frames)-1].get_color_frame()
        except:
            return None
        
    def pixel_to_point(self, colorFrame, x, y):
        currentFrame = None
        print()
        for frame in self.frames:
            print((time.time_ns()*(1/1000000.0))-colorFrame.get_timestamp(),(time.time_ns()*(1/1000000.0))-frame.get_color_frame().get_timestamp())
            if (time.time_ns()*(1/1000000.0))-colorFrame.get_timestamp()==(time.time_ns()*(1/1000000.0))-frame.get_color_frame().get_timestamp():
                currentFrame = frame
                break
        if currentFrame is None:
            print("Not found")
            return None
        depth = currentFrame.get_depth_frame().get_distance(x, y)
        print(depth)
        if depth <= 0: return None
        intr = self.profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
        return np.array(rs.rs2_deproject_pixel_to_point(intr, [x, y], depth))
        

                
