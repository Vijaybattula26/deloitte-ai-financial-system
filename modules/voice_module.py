# ==========================================================
# LEVEL-3 VOICE INPUT MODULE
# Converts Speech → Text for Financial AI Processing
# Supports multilingual speech (English, Hindi, Telugu)
# ==========================================================

import speech_recognition as sr


class VoiceProcessor:

    def __init__(self):

        self.recognizer = sr.Recognizer()


    # ======================================================
    # RECORD FROM MICROPHONE
    # ======================================================

    def listen(self, timeout=10, phrase_time_limit=15):

        try:

            with sr.Microphone() as source:

                print("Listening...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                print("Audio captured")

                print("Processing speech...")

                text = self.recognizer.recognize_google(
                    audio,
                    language="en-IN"
                )

                print("Recognized:", text)

                return {

                    "success": True,
                    "text": text

                }

        except sr.WaitTimeoutError:

            return {

                "success": False,
                "error": "Listening timeout"

            }

        except sr.UnknownValueError:

            return {

                "success": False,
                "error": "Could not understand speech"

            }

        except sr.RequestError:

            return {

                "success": False,
                "error": "Speech service unavailable"

            }

        except Exception as e:

            return {

                "success": False,
                "error": str(e)

            }


    # ======================================================
    # PROCESS AUDIO FILE
    # ======================================================

    def process_audio_file(self, file_path):

        try:

            with sr.AudioFile(file_path) as source:

                audio = self.recognizer.record(source)

                text = self.recognizer.recognize_google(
                    audio,
                    language="en-IN"
                )

                return {

                    "success": True,
                    "text": text

                }

        except Exception as e:

            return {

                "success": False,
                "error": str(e)

            }
