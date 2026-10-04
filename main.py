import kivy
kivy.require("2.3.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from datetime import datetime, timedelta
import threading
import os

from challenge_engine import get_random_challenge
from face_verification import verify_face
from register_face import register_face


class FaceAlarmApp(App):

    def build(self):

        self.alarm_time = None
        self.alarm_active = False
        self.challenge_popup = None

        self.alarm_sound = SoundLoader.load("alarm.wav")

        # -----------------------------
        # MAIN LAYOUT
        # -----------------------------

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="WAKEGUARD AI",
            font_size=40,
            bold=True
        )

        subtitle = Label(
            text="Intelligent wake-up verification system",
            font_size=18
        )

        # -----------------------------
        # REGISTER FACE BUTTON
        # -----------------------------

        register_button = Button(
            text="📷 REGISTER FACE",
            font_size=22,
            size_hint_y=None,
            height=60
        )

        register_button.bind(
            on_press=self.start_registration
        )

        # -----------------------------
        # TIME INPUT
        # -----------------------------

        self.time_input = TextInput(
            hint_text="Enter time (HH:MM)",
            font_size=25,
            multiline=False,
            halign="center",
            size_hint_y=None,
            height=60
        )

        # -----------------------------
        # SET ALARM BUTTON
        # -----------------------------

        set_button = Button(
            text="SET ALARM",
            font_size=22,
            size_hint_y=None,
            height=60
        )

        set_button.bind(
            on_press=self.set_alarm
        )

        # -----------------------------
        # STATUS
        # -----------------------------

        self.status = Label(
            text="Please register your face before using the alarm.",
            font_size=18
        )

        # -----------------------------
        # ADD WIDGETS
        # -----------------------------

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(register_button)
        layout.add_widget(self.time_input)
        layout.add_widget(set_button)
        layout.add_widget(self.status)

        return layout

    # =====================================================
    # FACE REGISTRATION
    # =====================================================

    def start_registration(self, instance):

        self.status.text = (
            "📷 Starting face registration...\n"
            "Please look at the camera."
        )

        threading.Thread(
            target=self.run_registration,
            daemon=True
        ).start()

    # =====================================================
    # RUN REGISTRATION
    # =====================================================

    def run_registration(self):

        result = register_face()

        Clock.schedule_once(
            lambda dt: self.registration_result(result)
        )

    # =====================================================
    # REGISTRATION RESULT
    # =====================================================

    def registration_result(self, result):

        if result:

            self.status.text = (
                "✅ Face registered successfully!\n"
                "You can now set your alarm."
            )

        else:

            self.status.text = (
                "❌ Face registration failed.\n"
                "Please try again."
            )

    # =====================================================
    # SET ALARM
    # =====================================================

    def set_alarm(self, instance):

        # Check whether face model exists

        if not os.path.exists("face_model.yml"):

            self.status.text = (
                "⚠️ Please register your face first."
            )

            return

        entered_time = self.time_input.text.strip()

        try:

            alarm_time = datetime.strptime(
                entered_time,
                "%H:%M"
            )

            now = datetime.now()

            alarm = now.replace(
                hour=alarm_time.hour,
                minute=alarm_time.minute,
                second=0,
                microsecond=0
            )

            if alarm <= now:
                alarm += timedelta(days=1)

            self.alarm_time = alarm
            self.alarm_active = True

            self.status.text = (
                "🔔 Alarm set for "
                + alarm.strftime("%I:%M %p")
            )

            Clock.schedule_interval(
                self.check_alarm,
                1
            )

        except ValueError:

            self.status.text = (
                "❌ Please enter time like 07:30"
            )

    # =====================================================
    # CHECK ALARM
    # =====================================================

    def check_alarm(self, dt):

        if not self.alarm_active:
            return

        now = datetime.now()

        if now >= self.alarm_time:

            self.alarm_active = False

            self.status.text = (
                "🚨 ALARM IS RINGING! 🚨\n\n"
                "Complete the wake-up challenge."
            )

            if self.alarm_sound:

                self.alarm_sound.loop = True
                self.alarm_sound.play()

            Clock.schedule_once(
                self.show_challenge,
                1
            )

    # =====================================================
    # SHOW CHALLENGE
    # =====================================================

    def show_challenge(self, dt):

        challenge = get_random_challenge()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        question = Label(
            text=challenge["question"],
            font_size=28
        )

        answer_input = TextInput(
            hint_text="Enter your answer",
            font_size=24,
            multiline=False,
            halign="center"
        )

        submit_button = Button(
            text="SUBMIT",
            font_size=22,
            size_hint_y=None,
            height=60
        )

        layout.add_widget(question)
        layout.add_widget(answer_input)
        layout.add_widget(submit_button)

        self.challenge_popup = Popup(
            title="🧠 WAKE UP CHALLENGE",
            content=layout,
            size_hint=(0.85, 0.6),
            auto_dismiss=False
        )

        def check_answer(instance):

            user_answer = answer_input.text.strip()

            correct_answer = str(
                challenge["answer"]
            ).strip()

            if user_answer.upper() == correct_answer.upper():

                self.challenge_popup.dismiss()

                self.status.text = (
                    "✅ Challenge completed!\n"
                    "📷 Starting face verification..."
                )

                threading.Thread(
                    target=self.run_face_verification,
                    daemon=True
                ).start()

            else:

                answer_input.text = ""

                question.text = (
                    "❌ Wrong answer!\n\n"
                    + challenge["question"]
                )

        submit_button.bind(
            on_press=check_answer
        )

        self.challenge_popup.open()

    # =====================================================
    # FACE VERIFICATION
    # =====================================================

    def run_face_verification(self):

        print("Starting face verification...")

        result = verify_face()

        Clock.schedule_once(
            lambda dt: self.face_verification_result(result)
        )

    # =====================================================
    # FACE VERIFICATION RESULT
    # =====================================================

    def face_verification_result(self, result):

        if result:

            if self.alarm_sound:
                self.alarm_sound.stop()

            self.status.text = (
                "✅ FACE VERIFIED!\n"
                "🎉 Wake-up verification successful!"
            )

            print("Wake-up verification successful.")

        else:

            self.status.text = (
                "❌ Face verification failed.\n"
                "🚨 Alarm continues!"
            )

            print("Face verification failed.")

            Clock.schedule_once(
                self.show_challenge,
                1
            )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    FaceAlarmApp().run()