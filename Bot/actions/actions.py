from typing import Any, Text, Dict, List
import json
from typedb.driver import TypeDB, SessionType, TransactionType
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionRechercherRestaurant(Action):
    def name(self) -> str:
        return "action_rechercher_restaurant"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Reinitialisation des slots
        # Extraction des slots pertinents
        cuisine = tracker.get_slot('cuisine')
        table_exterieur = tracker.get_slot('table_exterieur')
        hotel = tracker.get_slot('hotel')

        # Création de la requête TypeDB
        query = self.build_query(cuisine, table_exterieur, hotel)
        
        # Envoi de la requête à TypeDB
        restaurants = self.query_typedb(query)
        
        if restaurants:
            response = "Voici les restaurants trouvés :\n" + restaurants
        else:
            response = "Aucun restaurant trouvé avec les critères spécifiés."

        dispatcher.utter_message(response)
        return [SlotSet("cuisine", None), SlotSet("table_exterieur", None), SlotSet("hotel", None)]

    def build_query(self, cuisine, table_exterieur, hotel):
        query = "match $r isa restaurant"
        if cuisine:
            query += f"; $r has cuisine '{cuisine}'"
        if table_exterieur is not None:
            query += f"; $r has table-exterieur true"
        if hotel:
            query += f"; $h isa hotel, has nom '{hotel}'"
            query += f"; (hotel: $h, restaurant: $r) isa proximite"
        query += "; fetch $r: nom;"
        return query

    def query_typedb(self, query):
        list_restaurants = ""
        with TypeDB.core_driver("localhost:1729") as client:
            with client.session("agence-de-voyage", SessionType.DATA) as session:
                with session.transaction(TransactionType.READ) as transaction:
                    answer_iterator = transaction.query.fetch(query)
                    for i, JSON in enumerate(answer_iterator, start=1):
                        nom_value = JSON.get('r', {}).get('nom', [{}])[0].get('value', 'N/A')
                        list_restaurants += f"Restaurant #{i}: {nom_value}\n"
                    print("Requete envoyé")
        return list_restaurants

class ActionRechercherHotel(Action):
    def name(self) -> str:
        return "action_rechercher_hotel"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Reinitialisation des slots
        # Extraction des slots pertinents
        restaurant = tracker.get_slot('restaurant')
        petit_dejeuner = tracker.get_slot('petit-dejeuner')
        ville = tracker.get_slot('ville')
        wifi = tracker.get_slot('wifi')
        piscine = tracker.get_slot('piscine')

        print(restaurant)
        print(petit_dejeuner)
        print(ville)
        print(wifi)
        print(piscine)

        # Création de la requête TypeDB
        query = self.build_query(restaurant, petit_dejeuner, ville, wifi, piscine)
        
        # Envoi de la requête à TypeDB
        hotel = self.query_typedb(query)
        
        if hotel:
            response = "Voici les hotels trouvés :\n" + hotel
        else:
            response = "Aucun hotel trouvé avec les critères spécifiés."

        dispatcher.utter_message(response)
        return [SlotSet("restaurant", None), SlotSet("petit-dejeuner", None), SlotSet("ville", None), SlotSet("wifi", None), SlotSet("piscine", None)]

    def build_query(self, restaurant, petit_dejeuner, ville, wifi, piscine):
        query = "match $h isa hotel"
        if restaurant:
            query += f"; $r isa restaurant, has nom '{restaurant}'"
            query += f"; (restaurant: $r, hotel: $h) isa proximite"
        if petit_dejeuner is not None:
            query += f"; $h has petit-dejeuner true"
        if ville:
            query += f"; $h has ville '{ville}'"
        if wifi:
            query += f"; $h has wifi true"
        if piscine:
            query += f"; $h has piscine true"
        query += "; fetch $h: nom;"
        return query

    def query_typedb(self, query):
        list_restaurants = ""
        with TypeDB.core_driver("localhost:1729") as client:
            with client.session("agence-de-voyage", SessionType.DATA) as session:
                with session.transaction(TransactionType.READ) as transaction:
                    answer_iterator = transaction.query.fetch(query)
                    for i, JSON in enumerate(answer_iterator, start=1):
                        nom_value = JSON.get('h', {}).get('nom', [{}])[0].get('value', 'N/A')
                        list_restaurants += f"Hotel #{i}: {nom_value}\n"
                    print("Requete envoyé")
        return list_restaurants