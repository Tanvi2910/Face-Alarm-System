import cv2
import os

MODEL_PATH = "face_model.yml"

# -----------------------------
# FACE DETECTOR
# -----------------------------

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def verify_face():

    # -----------------------------
    # CHECK MODEL
    # -----------------------------

    if not os.path.exists(MODEL_PATH):
        print("Face model not found.")
        return False

    # -----------------------------
    # LOAD MODEL
    # -----------------------------

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read(MODEL_PATH)

    # -----------------------------
    # OPEN CAMERA
    # -----------------------------

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Camera could not be opened.")
        return False

    print("Camera started.")
    print("Looking for registered face...")

    verified_frames = 0
    required_frames = 5

    verified = False

    # -----------------------------
    # CAMERA LOOP
    # -----------------------------

    while True:

        ret, frame = camera.read()

        if not ret:
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

        # -----------------------------
        # NO FACE
        # -----------------------------

        if len(faces) == 0:

            verified_frames = 0

            cv2.putText(
                frame,
                "FACE NOT DETECTED",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # -----------------------------
        # FACE DETECTED
        # -----------------------------

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]

            label, confidence = recognizer.predict(face)

            # Our current threshold
            if confidence < 100:

                verified_frames += 1

                text = (
                    f"KNOWN FACE "
                    f"{verified_frames}/{required_frames}"
                )

                box_color = (0, 255, 0)

                if verified_frames >= required_frames:

                    verified = True

            else:

                verified_frames = 0

                text = "UNKNOWN PERSON"

                box_color = (0, 0, 255)

            # -----------------------------
            # DRAW BOX
            # -----------------------------

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                box_color,
                2
            )

            cv2.putText(
                frame,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                box_color,
                2
            )

            cv2.putText(
                frame,
                f"Score: {confidence:.1f}",
                (x, y + h + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                box_color,
                2
            )

        # -----------------------------
        # SHOW CAMERA
        # -----------------------------

        cv2.imshow(
            "WAKE ALARM - Face Verification",
            frame
        )

        # -----------------------------
        # FACE VERIFIED
        # -----------------------------

        if verified:

            print("FACE VERIFIED!")

            camera.release()
            cv2.destroyAllWindows()

            return True

        # -----------------------------
        # EXIT
        # -----------------------------

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break

    camera.release()
    cv2.destroyAllWindows()

    return False


# -----------------------------
# TEST
# -----------------------------

if __name__ == "__main__":

    result = verify_face()

    if result:
        print("SUCCESS: Registered face verified.")

    else:
        print("FAILED: Face verification failed.")