import cv2
from imutils import face_utils
import dlib
import os
import logging

def predict(rec, gray, x, y, h, w):
    prediction = rec.predict(gray[y:y + h, x:x + w])
    logging.info(prediction)
    return prediction

def add_predicted_text(image, x, y, h, w):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if id == 2:
        text = "Thank you for saving other's life"
        cv2.putText(image, text, (x, y + h + 50), font, 1, (255, 255, 255), 4, cv2.LINE_AA)
    elif id == 1:
        text = "Wear your mask"
        cv2.putText(image, text, (x, y + h + 50), font, 1, (255, 255, 255), 4, cv2.LINE_AA)

def add_face_mask(image, shape, x1, x2, y1, y2):
    threshold = 30
    cv2.rectangle(image, (x1 - threshold, y1 - threshold), (x2 + threshold, y2 + threshold), (255, 0, 0), 2)
    start_x, start_y = 0, 0
    count = 0
    numbers = [0, 17, 22, 27, 31, 36, 42, 48]
    for (x, y) in shape:
        if count in numbers:
            start_x, start_y = x, y
        else:
            cv2.line(image, (start_x, start_y), (x, y), (0, 255, 0), 1)
            start_x, start_y = x, y
        cv2.circle(image, (x, y), 1, (0, 255, 0), -1)
        count += 1

def execute(trained_model_path, face_landmark_model_path):
    face_landmark_model_path = face_landmark_model_path 
    trained_model_path = trained_model_path

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_model_path)
    cap = cv2.VideoCapture(0)

    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read(trained_model_path)

    while True:
        _, image = cap.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            x1, y1 = rect.left(), rect.top()
            x2, y2 = rect.right(), rect.bottom()
            x, y = x1, y1
            w, h = x2-x1, y2-y1
            id, conf = predict(rec, gray, x, y, h, w)
            add_predicted_text(image, x, y, h, w)
            add_face_mask(image, shape, x1, x2, y1, y2)

        cv2.imshow("Output", image)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    cap.release()
    return

def main(args):
    if args['component'] == 'prediction':
        parameters = args['parameters']
        dir = os.path.dirname(os.path.realpath(__file__)).split('/')
        dir = dir[1:len(dir)-2]
        base_url = ''
        for i in dir:
            base_url += ('/' + i)
        trained_model_path = base_url + parameters['trained_model_path'] 
        face_landmark_model_path = base_url + parameters['face_landmark_model_path']
        return execute(trained_model_path, face_landmark_model_path)