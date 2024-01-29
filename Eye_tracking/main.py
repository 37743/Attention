import numpy as np
import cv2



cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 2)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    roi_gray_face_left = np.array([])
    roi_color_face_left = np.array([])
    roi_color_eye_left = np.array([])

    roi_gray_face_right = np.array([])
    roi_color_face_right = np.array([])
    roi_color_eye_right = np.array([])

    if len(faces) == 0:
        # No faces detected, you might want to handle this case
        pass
    else:
        # Get the face
        for (x, y, w, h) in faces:

            # Left part of the face
            roi_gray_face_left = gray[y:y + h, x:(x + w // 2)]
            roi_color_face_left = frame[y:y + h, x:(x + w // 2)]

            # Right part of the face
            roi_gray_face_right = gray[y:y + h, (x + w // 2): (x + w)]
            roi_color_face_right = frame[y:y + h, (x + w // 2): (x + w)]

            # get the left eye
            eyes_left = eye_cascade.detectMultiScale(roi_gray_face_left, 1.3, 5)
            for (ex, ey, ew, eh) in eyes_left:
                roi_color_eye_left = roi_color_face_left[ey:ey + eh, ex:(ex + ew)]

            # get the right eye
            eyes_right = eye_cascade.detectMultiScale(roi_gray_face_right, 1.3, 5)
            for (ex, ey, ew, eh) in eyes_right:
                roi_color_eye_right = roi_color_face_right[ey:ey + eh, ex:(ex + ew)]

    if (roi_color_eye_left == 0).all():
        pass
    else:
        roi_color_eye_left = cv2.resize(roi_color_eye_left, None, fx=4, fy=4)
        cv2.imshow('left_eye', roi_color_eye_left)
        cv2.imshow('left_face', roi_color_face_left)

    if (roi_color_eye_right == 0).all():
        pass
    else:
        roi_color_eye_right = cv2.resize(roi_color_eye_right, None, fx=4, fy=4)
        cv2.imshow('right_eye', roi_color_eye_right)
        cv2.imshow('right_face', roi_color_face_right)

    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
