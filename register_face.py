import cv2
import os
import numpy as np

DATASET_PATH = "face_data"
MODEL_PATH = "face_model.yml"

def register_face():

    os.makedirs(DATASET_PATH, exist_ok=True)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Camera could not be opened.")
        return False

    print("📷 Face registration started.")
    print("Look at the camera.")

    sample_count = 0
    max_samples = 30

    while True:

        ret, frame = camera.read()

        if not ret:
            print("❌ Could not read camera.")
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]

            if sample_count < max_samples:

                sample_count += 1

                filename = os.path.join(
                    DATASET_PATH,
                    f"user_{sample_count}.jpg"
                )

                cv2.imwrite(
                    filename,
                    face
                )

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            f"Samples: {sample_count}/{max_samples}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "WakeGuard AI - Face Registration",
            frame
        )

        if sample_count >= max_samples:
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    if sample_count < max_samples:
        print("❌ Registration incomplete.")
        return False

    # -----------------------------
    # TRAIN FACE MODEL
    # -----------------------------

    faces_data = []
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

                faces_data.append(image)
                labels.append(1)

    if len(faces_data) == 0:

        print("❌ No face samples found.")
        return False

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.train(
        faces_data,
        np.array(labels)
    )

    recognizer.write(
        MODEL_PATH
    )

    print("✅ Face registration completed.")
    print("✅ Face model created.")

    return True


if __name__ == "__main__":

    result = register_face()

    if result:
        print("🎉 Registration successful!")
    else:
        print("❌ Registration failed.")