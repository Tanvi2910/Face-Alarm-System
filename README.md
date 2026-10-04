# FACE ALARM

A smart alarm application that uses face verification and wakefulness challenges to prevent accidental dismissal of alarms.

## Features

- Set an alarm using HH:MM format
- Face verification before stopping the alarm
- Wakefulness challenges for additional verification
- Camera-based identity verification
- Custom alarm sound
- Python-based desktop application

## Technologies Used

- Python
- OpenCV
- Kivy
- Computer Vision
- Face Recognition

## Project Structure

- `main.py` – Main application
- `face_verification.py` – Face verification
- `challenge_engine.py` – Wakefulness challenge system
- `register_face.py` – Face registration
- `recognize_face.py` – Face recognition
- `camera_test.py` – Camera testing

## How It Works

1. The user sets an alarm.
2. When the alarm rings, the application activates verification.
3. The user must complete identity verification.
4. Wakefulness challenges can be used as an additional verification step.
5. The alarm stops only after successful verification.

## Future Improvements

- Improved eye-state detection
- More wakefulness challenges
- Better recognition accuracy
- Mobile application support
- Improved user interface