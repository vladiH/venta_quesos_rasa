from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, FormValidationAction, Action, ValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.types import DomainDict

from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
import sqlite3

# change this to the location of your SQLite file
path_to_db = "actions/quesos.db"

class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get slots and save as tuple
        product = [(tracker.get_slot("cheese")), (tracker.get_slot("brand"))]
        
        # place cursor on correct row based on search criteria
        cursor.execute("SELECT * FROM inventory WHERE cheese=? AND brand=?", product)
        
        # retrieve sqlite row
        data_row = cursor.fetchone()
        if data_row:
            # provide in stock message
            dispatcher.utter_message(template="utter_in_stock")
            connection.close()
            slots_to_reset = ["cheese", "brand"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            dispatcher.utter_message(template="utter_no_stock")
            connection.close()
            slots_to_reset = ["cheese", "brand"]
            return [SlotSet(slot, None) for slot in slots_to_reset]

class SurveySubmit(Action):
    def name(self) -> Text:
        return "action_survey_submit"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_survey_end")
        return [SlotSet("survey_complete", True)]