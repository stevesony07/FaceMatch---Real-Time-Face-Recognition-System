import cv2
from deepface import DeepFace
import os
import threading

# Directory where images are saved
dataset_dir = r"C:\Users\steve\OneDrive\Desktop\Learn\python\colgproject\joe\dataset"

def load_reference_images():
    reference_images = {}
    for person_name in os.listdir(dataset_dir):
        person_dir = os.path.join(dataset_dir, person_name)
        if os.path.isdir(person_dir):
            for img_name in os.listdir(person_dir):
                img_path = os.path.join(person_dir, img_name)
                reference_images[img_path] = person_name
    return reference_images

reference_images = load_reference_images()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
face_match = False
matched_name = "Unknown"

def check_face(frame):
    global face_match, matched_name
    for img_path, name in reference_images.items():
        try:
            result = DeepFace.verify(frame, cv2.imread(img_path))
            if result['verified']:
                face_match = True
                matched_name = name
                return
        except ValueError as e:
            print(f"Error verifying face: {e}")
    face_match = False
    matched_name = "Unknown"

while True:
    ret, frame = cap.read()

    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError as e:
                print(f"Error starting thread: {e}")
        counter += 1

        if face_match:
            cv2.putText(frame, matched_name, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "No Match", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
 
