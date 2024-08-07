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
        list_hotels = ""
        with TypeDB.core_driver("localhost:1729") as client:
            with client.session("agence-de-voyage", SessionType.DATA) as session:
                with session.transaction(TransactionType.READ) as transaction:
                    answer_iterator = transaction.query.fetch(query)
                    for i, JSON in enumerate(answer_iterator, start=1):
                        nom_value = JSON.get('h', {}).get('nom', [{}])[0].get('value', 'N/A')
                        list_hotels += f"Hotel #{i}: {nom_value}\n"
                    print("Requete envoyé")
        return list_hotels
    
class ActionDetailRestaurant(Action):
    def name(self) -> str:
        return "action_detail_restaurant"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Extraction des slots pertinents
        cuisine = tracker.get_slot('cuisine')
        table_exterieur = tracker.get_slot('table_exterieur')
        restaurant = tracker.get_slot('restaurant')
        prix = tracker.get_slot('prix')

        # Création de la requête TypeDB
        query = self.build_query(restaurant)
        
        # Envoi de la requête à TypeDB
        details = self.query_typedb(query, cuisine, table_exterieur, prix)
        if details:
            response = f"Voici les informations du restaurant {restaurant} :\n" + details
        else:
            response = "Je suis désolé mais je n'ai pas pu trouver d'informations a propos de ce restaurant."

        dispatcher.utter_message(response)
        return [SlotSet("cuisine", None), SlotSet("table_exterieur", None), SlotSet("restaurant", None), SlotSet("prix", None)]

    def build_query(self, restaurant):
        query = f"match $r isa restaurant, has nom '{restaurant}'; fetch $r: cuisine, table-exterieur, prix;"
        return query

    def query_typedb(self, query, cuisine, table_exterieur, prix):
        list_detail = ""
        with TypeDB.core_driver("localhost:1729") as client:
            with client.session("agence-de-voyage", SessionType.DATA) as session:
                with session.transaction(TransactionType.READ) as transaction:
                    answer_iterator = transaction.query.fetch(query)
                    for i, JSON in enumerate(answer_iterator, start=1):
                        if cuisine:
                            cuisine_value = JSON.get('r', {}).get('cuisine', [{}])[0].get('value', 'N/A')
                            list_detail += f"Type de cuisine: {cuisine_value}\n"
                        if table_exterieur:
                            table_exterieur_value = JSON.get('r', {}).get('table-exterieur', [{}])[0].get('value', 'N/A')
                            if table_exterieur_value == True:
                                table_exterieur_value = "Oui"
                            else:
                                table_exterieur_value = "Non"
                            list_detail += f"Table exterieur: {table_exterieur_value}\n"
                        if prix:
                            prix_value = JSON.get('r', {}).get('prix', [{}])[0].get('value', 'N/A')
                            list_detail += f"Prix: {prix_value}\n"
                    print("Requete envoyé")
        return list_detail
    
class ActionDetailCompletRestaurant(Action):
    def name(self) -> str:
        return "action_detail_complet_restaurant"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Extraction des slots pertinents
        restaurant = tracker.get_slot('restaurant')

        # Création de la requête TypeDB
        query = self.build_query(restaurant)
        
        # Envoi de la requête à TypeDB
        details = self.query_typedb(query)
        if details:
            response = f"Voici les informations du restaurant {restaurant} :\n" + details
            dispatcher.utter_message(response)
        else:
            response = "Je suis désolé mais je n'ai pas pu trouver d'informations a propos de ce restaurant."
            dispatcher.utter_message(buttons={"title":"Recherche approfondie", "payload":"details_complet_restaurant"},response=response)

        return [SlotSet("restaurant", None)]

    def build_query(self, restaurant):
        query = f"match $r isa restaurant, has nom '{restaurant}'; fetch $r: cuisine, table-exterieur, prix;"
        return query

    def query_typedb(self, query):
        list_detail = ""
        with TypeDB.core_driver("localhost:1729") as client:
            with client.session("agence-de-voyage", SessionType.DATA) as session:
                with session.transaction(TransactionType.READ) as transaction:
                    answer_iterator = transaction.query.fetch(query)
                    for i, JSON in enumerate(answer_iterator, start=1):
                        cuisine_value = JSON.get('r', {}).get('cuisine', [{}])[0].get('value', 'N/A')
                        table_ext_value = JSON.get('r', {}).get('cuisine', [{}])[0].get('value', 'N/A')
                        if table_ext_value == True:
                            table_ext_value = "Oui"
                        else:
                            table_ext_value = "Non"
                        prix_value = JSON.get('r', {}).get('cuisine', [{}])[0].get('value', 'N/A')
                        list_detail += f" Type de cuisine: {cuisine_value}\n"
                        list_detail += f" Terrace: {cuisine_value}\n"
                        list_detail += f" Catégorie de prix: {prix_value}\n"
                    print("Requete envoyé")
        return list_detail