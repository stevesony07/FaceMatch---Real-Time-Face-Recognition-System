import cv2
import os

# Directory to save images
dataset_dir = "dataset"
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Press 's' to save an image, 'q' to quit.")

while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow("Capture Image", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            name = input("Enter the name of the person: ")
            if name:
                person_dir = os.path.join(dataset_dir, name)
                if not os.path.exists(person_dir):
                    os.makedirs(person_dir)
                img_path = os.path.join(person_dir, f"{name}_{len(os.listdir(person_dir)) + 1}.jpg")
                cv2.imwrite(img_path, frame)
                print(f"Saved {img_path}")
        elif key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
