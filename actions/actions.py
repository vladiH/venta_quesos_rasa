from typing import Any, Text, Dict, List, Union
from rasa_sdk import Tracker, FormValidationAction, Action, ValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.types import DomainDict

from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
import sqlite3

# change this to the location of your SQLite file
path_to_db = "actions/quesos.db"

COLUMNS_INVENTORY = ['QUESO', 'MARCA', 'PRECIO', 'Kg']
class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"
    
    @staticmethod 
    def required_slots(tracker): 
        return ["brand"]

    def slot_mapping(self) -> Dict[Text, Union[Dict,List[Dict]]]:
        return {"brand": [self.from_text()]}

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
        product = [(tracker.get_slot("cheese").lower()), (tracker.get_slot("brand").lower())]
        
        # place cursor on correct row based on search criteria
        cursor.execute("SELECT * FROM inventory WHERE cheese=? OR brand=?", product)
        
        # retrieve sqlite row
        data_rows = cursor.fetchall()
        if len(data_rows)==1:
            # provide in stock message
            dispatcher.utter_message(template="utter_in_stock")
            dispatcher.utter_message(text='\n'.join(['{}: {}'.format(k,v) for (k, v) in zip(COLUMNS_INVENTORY, data_rows)]))
            connection.close()
            slots_to_reset = ["cheese", "brand"]
            return [SlotSet(slot, None) for slot in slots_to_reset]

        elif len(data_rows)>1:
            # provide in stock message
            dispatcher.utter_message(template="utter_in_stocks")
            for row in data_rows:
                dispatcher.utter_message(text='\n'.join(['{}: {}'.format(k,v) for (k, v) in zip(COLUMNS_INVENTORY, row)]))
            connection.close()
            slots_to_reset = ["cheese", "brand"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            dispatcher.utter_message(template="utter_no_stock")
            connection.close()
            slots_to_reset = ["cheese", "brand"]
            return [SlotSet(slot, None) for slot in slots_to_reset]

class OrderStatus(Action):
    def name(self) -> Text:
        return "action_order_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email").lower(),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # convert tuple to list
            data_list = list(data_row)

            # respond with order status
            dispatcher.utter_message(template="utter_order_status", status=data_list[5], date=data_list[0], code=data_list[1])
            dispatcher.utter_message(template="utter_success_presubmit")
            connection.close()
            return [SlotSet("is_ok", True), SlotSet("email", None)]
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
            return [SlotSet("email", None)]
            
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