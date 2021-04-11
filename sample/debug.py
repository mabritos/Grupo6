import cv2
import time

class Debug(object):
    def __init__(self):
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.frame = None
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def fps(self, frame):
        self.frame = frame
        
        # time when we finish processing for this frame
        self.new_frame_time = time.time()
    
        # Calculating the fps
    
        # fps will be number of frame processed in given time frame
        # since their will be most of time error of 0.001 second
        # we will be subtracting it to get more accurate result
        fps = 1/(self.new_frame_time-self.prev_frame_time)
        self.prev_frame_time = self.new_frame_time
    
        # converting the fps into integer
        fps = int(fps)
    
        # converting the fps to string so that we can display it on frame
        # by using putText function
        fps = str(fps)
    
        # puting the FPS count on the frame
        cv2.putText(self.frame, fps, (7, 70), self.font, 3, (100, 255, 0), 3, cv2.LINE_AA)

        return self.frame