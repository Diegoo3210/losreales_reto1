from imageai.Detection.Custom import CustomObjectDetection
from datetime import timedelta
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath('yolov3.pt')
#detector.loadModel()

def get_frame_info(frame):
  detections = detector.detectObjectsFromImage(input_image=frame)
  for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])

def detect_objects_in_video(video_path, output_path):
  f=open(output_path, "w")
  SAVING_FRAMES_PER_SECOND = 1

  def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s
  cap = cv2.VideoCapture(video_path)
  # get the FPS of the video
  fps = cap.get(cv2.CAP_PROP_FPS)
  # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
  saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
  # get the list of duration spots to save
  saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
  # start the loop
  count = 0
  while True:
      is_read, frame = cap.read()
      if not is_read:
          # break out of the loop if there are no frames to read
          break
      # get the duration by dividing the frame count by the FPS
      frame_duration = count / fps
      try:
          # get the earliest duration to save
          closest_duration = saving_frames_durations[0]
      except IndexError:
          # the list is empty, all duration frames were saved
          break
      if frame_duration >= closest_duration:
          # if closest duration is less than or equals the frame duration, 
          # then save the frame
          plt.imshow(frame)
          plt.show() 
          # drop the duration spot from the list, since this duration spot is already saved
          try:
              saving_frames_durations.pop(0)
          except IndexError:
              pass
      # increment the frame count
      count += 1

  
  f.close()