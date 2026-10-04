import cv2

# Load face detection model
face_cascade = cv2.CascadeClassifier(
    r"C:\Users\Tanvi\AppData\Local\Python\pythoncore-3.12-64\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"
)

# Open camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

print("Face detection started. Press Q to close.")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Could not read camera.")
        break

    # Convert camera image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    # Draw box around detected face
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    # Show camera
    cv2.imshow("FACE ALARM - Face Detection", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()