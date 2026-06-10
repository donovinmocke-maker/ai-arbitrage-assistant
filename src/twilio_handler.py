from src.grok_assistant import GrokAssistant
import os
from dotenv import load_dotenv

load_dotenv()

class TwilioHandler:
    def __init__(self):
        self.assistant = GrokAssistant()
        self.consent_sent = {}  # Track which numbers have received consent

        self.consent_message = """By providing your phone number to CC Palms LLC, you consent to receive SMS messages regarding appointments, project updates, estimates, and special offers. Message and data rates may apply. Reply STOP at any time to opt out."""

    def handle_incoming_sms(self, from_number, body):
        # First time interaction - send consent
        if from_number not in self.consent_sent:
            self.consent_sent[from_number] = True
            consent_intro = f"Welcome to CC Palms LLC! {self.consent_message}\n\n"
            response = self.assistant.get_response(body, from_number)
            return consent_intro + response

        # Normal conversation
        return self.assistant.get_response(body, from_number)
