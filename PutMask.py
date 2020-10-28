import cv2
import numpy as np
import  dlib
from math import hypot
import  os

def PutMaskInFace(ImageName,Mask,OutDir):

    # Load img
    img = cv2.imread(ImageName)
    mask_image = cv2.imread(Mask)
    img = cv2.resize(img,(0,0),None,0.5,0.5)
    imgOrginal = img.copy()
    # Loading Face detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = detector(imgGray)
    for face in faces:
        landmarks = predictor(imgGray, face)
        # Mask coordinates
        top_nose = (landmarks.part(29).x, landmarks.part(29).y)
        center_mouth = (landmarks.part(51).x, landmarks.part(51).y)
        left_face = (landmarks.part(3).x, landmarks.part(3).y)
        right_face = (landmarks.part(13).x, landmarks.part(13).y)
        face_width = int(hypot(left_face[0] - right_face[0],
                        left_face[1] - right_face[1]) * 1.25)
        face_mouth_height = int(face_width * 0.8)
        # New nose position
        top_left = (int(center_mouth[0] - face_width / 2),
                                int(center_mouth[1] - face_mouth_height / 2))
        bottom_right = (int(center_mouth[0] + face_width / 2),
                        int(center_mouth[1] + face_mouth_height / 2))
        
        # Adding the new nose
        mask_mouth = cv2.resize(mask_image, (face_width, face_mouth_height))
        mask_mouth_gray = cv2.cvtColor(mask_mouth, cv2.COLOR_BGR2GRAY)
        _, mouth_mask = cv2.threshold(mask_mouth_gray, 25, 255, cv2.THRESH_BINARY_INV)
        nose_area = imgOrginal[top_left[1]: top_left[1] + face_mouth_height,
                    top_left[0]: top_left[0] + face_width]
        nose_area_no_nose = cv2.bitwise_and(nose_area, nose_area, mask=mouth_mask)
        final_mouth = cv2.add(nose_area_no_nose, mask_mouth)
        imgOrginal[top_left[1]: top_left[1] + face_mouth_height,
                        top_left[0]: top_left[0] + face_width] = final_mouth
    # cv2.imshow("Orginal",imgOrginal)
    cv2.imwrite(OutDir , imgOrginal)
    # cv2.waitKey(0)

