from objectTracking import objectTracking
import cv2

# Difficulty: 0 for Easy, 1 for Medium
difficulty = input('Enter the difficult level, 0 for Easy, 1 for Medium: ')
difficulty = int(difficulty)

if difficulty == 1:
    obj = cv2.VideoCapture("Medium.mp4")
    objectTracking(obj, difficulty)
    obj.release()
elif difficulty == 0:
    obj = cv2.VideoCapture("Easy.mp4")
    objectTracking(obj, difficulty)
    obj.release()
