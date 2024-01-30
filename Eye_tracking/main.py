# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Eye/Gaze Tracking Code
# ---
import cv2
import numpy as np
import mediapipe as mp
from utilities import LEFT_EYE, RIGHT_EYE, euclideanDistance

DISABLED = False
TOTAL_BLINKS =0

class GazeTracker():
    def gaze_ratio(frame, eye, landmarks, frame_h, frame_w):
        ''' Extracts and thresholds the eyes' regions,
        increases the contrast, then calculates the ratio
        of the white pixels to the black pixels divided at the
        center of the frame. This is used to determine
        whether the eye(s) extracted are looking to the right,
        center, or left direction.

        @eye Either 1 or 0, where 0 denotes left eye.'''
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        choice = LEFT_EYE if eye == 0 else RIGHT_EYE
        left_eye_region = np.array([(int(landmarks[i].x*frame_w), int(landmarks[i].y*frame_h)) for i in choice])
        mask = np.zeros((frame_h, frame_w), np.uint8)
        cv2.polylines(mask, [left_eye_region], True, 255, 2)
        cv2.fillPoly(mask, [left_eye_region], 255)
        left_eye = cv2.bitwise_and(gray, gray, mask=mask)
        left_eye = cv2.equalizeHist(left_eye)

        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])

        gray_eye = left_eye[min_y: max_y, min_x: max_x]
        _, threshold_eye = cv2.threshold(gray_eye, 100, 255, cv2.THRESH_BINARY)
        threshold_h, threshold_w = threshold_eye.shape
        lthresh = threshold_eye[0: threshold_h, 0: int(threshold_w/2)]
        lthresh_white = cv2.countNonZero(lthresh)
        rthresh = threshold_eye[0: threshold_h, int(threshold_w/2): threshold_w]
        rthresh_white = cv2.countNonZero(rthresh)
        gaze_ratio = lthresh_white/rthresh_white
        return gaze_ratio

    def closed_ratio(frame, landmarks, right_indices, left_indices):
        ''' Defines the ratio of the horizontal and vertical line
        to which determine whether the eye seems to be closed/blinking.'''
        # horizontal
        rh_right = landmarks[right_indices[0]]
        rh_left = landmarks[right_indices[8]]
        # vertical
        rv_top = landmarks[right_indices[12]]
        rv_bottom = landmarks[right_indices[4]]
        cv2.line(frame, rh_right, rh_left, (0,255,0), 2)
        cv2.line(frame, rv_top, rv_bottom, (0,255,255), 2)
        # horizontal line 
        lh_right = landmarks[left_indices[0]]
        lh_left = landmarks[left_indices[8]]
        # vertical line 
        lv_top = landmarks[left_indices[12]]
        lv_bottom = landmarks[left_indices[4]]
        cv2.line(frame, lh_right, lh_left, (0,255,0), 2)
        cv2.line(frame, lv_top, lv_bottom, (0,255,255), 2)
        # euclidean distances
        rhDistance = euclideanDistance.solve(rh_right, rh_left)
        rvDistance = euclideanDistance.solve(rv_top, rv_bottom)
        lvDistance = euclideanDistance.solve(lv_top, lv_bottom)
        lhDistance = euclideanDistance.solve(lh_right, lh_left)
        try:
            reRatio = rhDistance/rvDistance
        except ZeroDivisionError:
            reRatio = 0
        try:
            leRatio = lhDistance/lvDistance
        except ZeroDivisionError:
            leRatio = 0
        ratio = (reRatio+leRatio)/2
        return ratio
    
    def __init__(self):
        # Captures the first device to cam-record.
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Video Capture Window", cv2.WINDOW_NORMAL) 
        cv2.resizeWindow("Video Capture Window", 512, 400)
        # Mediapipe's ready-made face mesh technology.
        face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        while True:
            _, frame = cap.read()
            # if not ret: 
            #     break
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = face_mesh.process(rgb_frame)
            frame_h, frame_w = frame.shape[:2]
            landmark_points = output.multi_face_landmarks
            if landmark_points:
                landmarks = landmark_points[0].landmark
                mesh_points = np.array([np.multiply([p.x, p.y],[frame_w, frame_h]).astype(int) for p in landmarks])
                gaze_ratio_l = self.gaze_ratio(frame, 0, landmarks, frame_h, frame_w)
                gaze_ratio_r = self.gaze_ratio(frame, 1, landmarks, frame_h, frame_w)
                avg_gaze_ratio = (gaze_ratio_l + gaze_ratio_r) / 2
                
                # Highlighting eyes with circles.
                ratio = self.closed_ratio(frame, mesh_points, RIGHT_EYE, LEFT_EYE)
                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_EYE])
                (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_EYE])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)
                cv2.circle(frame, center_left, int(l_radius*.5), (0,255,0), 2, cv2.LINE_AA)
                cv2.circle(frame, center_right, int(r_radius*.5), (0,255,0), 2, cv2.LINE_AA)

                # Flip and add text for direction clarity.
                frame = cv2.flip(frame, 1)
                if avg_gaze_ratio < 0.9:
                    print("RIGHT")
                    # cv2.putText(frame, 'RIGHT {f}'.format(f=avg_gaze_ratio), (50, frame_h-75), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
                elif 0.9 <= avg_gaze_ratio < 2:
                    print("CENTER")
                    # cv2.putText(frame, 'CENTER {f}'.format(f=avg_gaze_ratio), (50, frame_h-75), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
                else:
                    print("LEFT")
                    # cv2.putText(frame, 'LEFT {f}'.format(f=avg_gaze_ratio), (50, frame_h-75), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
                if ratio >5.5:
                    DISABLED = True
                    # cv2.putText(frame, 'Eye(s) Closed: {f}'.format(f=TOTAL_BLINKS), (50, 75), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
                else:
                    if DISABLED == True:
                        TOTAL_BLINKS +=1
                        DISABLED = not DISABLED
                # cv2.imshow("Video Capture Window", frame)
            if cv2.waitKey(1) == ord('q'):
            # Breaks if 'q' is pressed and ends program.
            # TODO: change this into a trigger event for the Kivy program.
                break
        cap.release()
        cv2.destroyAllWindows()
