import cv2
import os
import numpy as np

DATASET_PATH = "face_data"
MODEL_PATH = "face_model.yml"

# -----------------------------
# FACE DETECTOR
# -----------------------------

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# -----------------------------
# LOAD REGISTERED FACES
# -----------------------------

faces = []
labels = []

for filename in os.listdir(DATASET_PATH):

    if filename.endswith(".jpg"):

        image_path = os.path.join(
            DATASET_PATH,
            filename
        )

        image = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        if image is not None:
            faces.append(image)
            labels.append(1)

if len(faces) == 0:
    print("No face samples found.")
    exit()

print(f"{len(faces)} face samples loaded.")

# -----------------------------
# CREATE LBPH RECOGNIZER
# -----------------------------

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(
    faces,
    np.array(labels)
)

recognizer.write(MODEL_PATH)

print("Face model trained successfully.")

# -----------------------------
# OPEN CAMERA
# -----------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

print("Face recognition started.")
print("Press Q to exit.")

# 5-frame verification
verified_frames = 0
required_frames = 5

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    detected_faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    # If no face is detected, reset verification
    if len(detected_faces) == 0:
        verified_frames = 0

    for (x, y, w, h) in detected_faces:

        face = gray[y:y+h, x:x+w]

        # Recognize face
        label, confidence = recognizer.predict(face)

        # -----------------------------
        # CHECK IDENTITY
        # -----------------------------

        if confidence < 100:

            verified_frames += 1

            text = f"KNOWN ({verified_frames}/{required_frames})"
            box_color = (0, 255, 0)

            if verified_frames >= required_frames:
                text = "FACE VERIFIED!"

        else:

            verified_frames = 0

            text = "UNKNOWN PERSON"
            box_color = (0, 0, 255)

        # -----------------------------
        # DRAW FACE BOX
        # -----------------------------

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            box_color,
            2
        )

        # -----------------------------
        # DISPLAY RESULT
        # -----------------------------

        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            box_color,
            2
        )

        cv2.putText(
            frame,
            f"Score: {confidence:.1f}",
            (x, y+h+25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            box_color,
            2
        )

    # -----------------------------
    # SHOW CAMERA
    # -----------------------------

    cv2.imshow(
        "WAKE ALARM - Face Recognition",
        frame
    )

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()