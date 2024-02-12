# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Eye/Gaze Tracking Code
# ---
from cv2 import (cvtColor,
                 VideoCapture,
                 polylines,
                 fillPoly,
                 line,
                 equalizeHist,
                 bitwise_and,
                 threshold,
                 countNonZero,
                 minEnclosingCircle,
                 circle,
                 flip,
                 waitKey,
                 destroyAllWindows,
                 COLOR_BGR2RGB,
                 COLOR_BGR2GRAY,
                 THRESH_BINARY,
                 LINE_AA)
import numpy as np
import mediapipe as mp
from script.eyetracking.utilities import (LEFT_EYE,
                                          RIGHT_EYE,
                                          EuclideanDistance)
from time import sleep

DISABLED = False

# Penalty Counter
PENALTY = {'blinks':0,
           'left':0,
           'center':0,
           'right':0,
           'recent':""}

class Penalty:
    # Modules-wide Variables
    pause = False
    end = False
    reset = False
    def __init__(self):
        # TEMP
        self.blinks = 0
        self.left = 0
        self.center = 0
        self.right = 0
        self.recent = ""

    def update(self, penalty):
        self.blinks = penalty['blinks']
        self.left = penalty['left']
        self.center = penalty['center']
        self.right = penalty['right']
        self.recent = penalty['recent']

penalty = Penalty()

class GazeTracker:
    def _loc_status(self, avg_gr):
        global PENALTY
        if avg_gr < 0.65:
            PENALTY['right'] += 1
            return "right"
        elif 0.65 <= avg_gr < 2:
            print(avg_gr)
            PENALTY['center'] += 1
            return "center"
        else:
            PENALTY['left'] += 1
            return "left"

    def _blink_status(self, avg_br):
        global DISABLED
        global PENALTY
        if avg_br >5.5:
            DISABLED = True
            return ""
        else:
            if DISABLED == True:
                PENALTY['blinks'] +=1
                DISABLED = not DISABLED
                return "blinked"
            return ""
    
    def gaze_ratio(self, frame, eye, landmarks, frame_h, frame_w):
        ''' Extracts and thresholds the eyes' regions,
        increases the contrast, then calculates the ratio
        of the white pixels to the black pixels divided at the
        center of the frame. This is used to determine
        whether the eye(s) extracted are looking to the right,
        center, or left direction.

        @eye Either 1 or 0, where 0 denotes left eye.'''
        gray = cvtColor(frame, COLOR_BGR2GRAY)
        choice = LEFT_EYE if eye == 0 else RIGHT_EYE
        left_eye_region = np.array([(int(landmarks[i].x*frame_w), int(landmarks[i].y*frame_h)) for i in choice])
        mask = np.zeros((frame_h, frame_w), np.uint8)
        polylines(mask, [left_eye_region], True, 255, 2)
        fillPoly(mask, [left_eye_region], 255)
        left_eye = bitwise_and(gray, gray, mask=mask)
        left_eye = equalizeHist(left_eye)

        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])

        gray_eye = left_eye[min_y: max_y, min_x: max_x]
        _, threshold_eye = threshold(gray_eye, 100, 255, THRESH_BINARY)
        threshold_h, threshold_w = threshold_eye.shape
        lthresh = threshold_eye[0: threshold_h, 0: int(threshold_w/2)]
        lthresh_white = countNonZero(lthresh)
        rthresh = threshold_eye[0: threshold_h, int(threshold_w/2): threshold_w]
        rthresh_white = countNonZero(rthresh)
        gaze_ratio = lthresh_white/rthresh_white
        return gaze_ratio

    def closed_ratio(self, frame, landmarks, right_indices, left_indices):
        ''' Defines the ratio of the horizontal and vertical line
        to which determine whether the eye seems to be closed/blinking.'''
        # horizontal
        rh_right = landmarks[right_indices[0]]
        rh_left = landmarks[right_indices[8]]
        # vertical
        rv_top = landmarks[right_indices[12]]
        rv_bottom = landmarks[right_indices[4]]
        line(frame, rh_right, rh_left, (0,255,0), 2)
        line(frame, rv_top, rv_bottom, (0,255,255), 2)
        # horizontal line 
        lh_right = landmarks[left_indices[0]]
        lh_left = landmarks[left_indices[8]]
        # vertical line 
        lv_top = landmarks[left_indices[12]]
        lv_bottom = landmarks[left_indices[4]]
        line(frame, lh_right, lh_left, (0,255,0), 2)
        line(frame, lv_top, lv_bottom, (0,255,255), 2)
        # euclidean distances
        rhDistance = EuclideanDistance.solve(rh_right, rh_left)
        rvDistance = EuclideanDistance.solve(rv_top, rv_bottom)
        lvDistance = EuclideanDistance.solve(lv_top, lv_bottom)
        lhDistance = EuclideanDistance.solve(lh_right, lh_left)
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
        super(GazeTracker, self).__init__()
        self.cap = VideoCapture(0)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        while True:
            if (penalty.end):
                break
            if (penalty.pause):
                continue
            if (penalty.reset):
                global PENALTY
                PENALTY = {'blinks':0,
                            'left':0,
                            'center':0,
                            'right':0,
                            'recent':""}
                penalty.reset = not penalty.reset
            _, self.frame = self.cap.read()
            # if not ret: 
            #     break
            rgb_frame = cvtColor(self.frame, COLOR_BGR2RGB)
            self.output = self.face_mesh.process(rgb_frame)
            frame_h, frame_w = self.frame.shape[:2]
            landmark_points = self.output.multi_face_landmarks
            if landmark_points:
                landmarks = landmark_points[0].landmark
                mesh_points = np.array([np.multiply([p.x, p.y],[frame_w, frame_h]).astype(int) for p in landmarks])
                gaze_ratio_l = self.gaze_ratio(self.frame, 0, landmarks, frame_h, frame_w)
                gaze_ratio_r = self.gaze_ratio(self.frame, 1, landmarks, frame_h, frame_w)
                avg_gaze_ratio = (gaze_ratio_l + gaze_ratio_r) / 2
                
                # Highlighting eyes with circles.
                ratio = self.closed_ratio(self.frame, mesh_points, RIGHT_EYE, LEFT_EYE)
                (l_cx, l_cy), l_radius = minEnclosingCircle(mesh_points[LEFT_EYE])
                (r_cx, r_cy), r_radius = minEnclosingCircle(mesh_points[RIGHT_EYE])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)
                circle(self.frame, center_left, int(l_radius*.5), (0,255,0), 2, LINE_AA)
                circle(self.frame, center_right, int(r_radius*.5), (0,255,0), 2, LINE_AA)
            # Flip and add text for direction clarity.
            self.frame = flip(self.frame, 1)
            sleep(1)
            PENALTY['recent'] = self._loc_status(avg_gaze_ratio)
            self._blink_status(ratio)
            penalty.update(PENALTY)
            # if waitKey(1) == 27:
            # # Breaks if 'q' is pressed and ends program.
            #     break
        self.cap.release()
        destroyAllWindows()