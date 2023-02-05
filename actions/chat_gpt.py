import openai
import os
from dotenv import load_dotenv
from rasa_sdk import Action
from rasa_sdk.events import EventType, SlotSet

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ActionGPT3(Action):
    def name(self) -> str:
        return "action_gpt3"
    
    def run(self, dispatcher, tracker, domain):
        request = " ".join(tracker.latest_message['text'].split())
        print(request)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="a esta pregunta: {} Responde el tipo de queso que necesita y si puedes la marca. Todo en español".format(request),
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text
        dispatcher.utter_message(text=response)
        return []