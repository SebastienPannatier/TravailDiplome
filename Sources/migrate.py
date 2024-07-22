from typedb.driver import TypeDB, SessionType, TransactionType
import csv

def parse_data_to_dictionaries(input):
    items = []
    with open(input["data_path"]+".csv", encoding="UTF-8") as data:
        for row in csv.DictReader(data, skipinitialspace=True):
            item = {key.lstrip('\ufeff'): value for key, value in row.items()}
            items.append(item)
    return items


def hotel_template(hotel):
    # Insert hotel
    typeql_insert_query = 'insert $hotel isa hotel, has nom "'+ hotel["Nom"]+'"'
    typeql_insert_query += ', has prix "'+hotel["Prix"]+'"'
    typeql_insert_query += ', has petit-dejeuner '+hotel["Petit-dej"]+''
    typeql_insert_query += ', has ville "'+hotel["Ville"]+'"'
    typeql_insert_query += ', has wifi '+hotel["Wifi"]+''
    typeql_insert_query += ', has etoile '+hotel["Etoile"]+''
    typeql_insert_query += ', has piscine '+hotel["Piscine"]+';'
    return typeql_insert_query

def restaurant_template(restaurant):
    # Insert restaurant
    typeql_insert_query = 'insert $restaurant isa restaurant, has nom "'+restaurant["Nom"]+'"'
    typeql_insert_query += ', has cuisine "'+restaurant["Cuisine"]+'"'
    typeql_insert_query += ', has table-exterieur '+restaurant["Exterieur"]+''
    typeql_insert_query += ', has prix "'+restaurant["Prix"]+'";'
    return typeql_insert_query

def proximite_template(proximite):
    # Match hotel
    typeql_insert_query = 'match $hotel isa hotel, has nom "'+proximite["hotel"]+'";'
    # Match restaurant
    typeql_insert_query += ' $restaurant isa restaurant, has nom "'+proximite["restaurant"]+'";'
    # Insert proximite
    typeql_insert_query += ' insert $proximite(hotel: $hotel, restaurant: $restaurant) isa proximite;'
    return typeql_insert_query


def load_data_into_typedb(input, session):
    items = parse_data_to_dictionaries(input)
    
    for item in items:
        with session.transaction(TransactionType.WRITE) as transaction:
            typeql_insert_query = input["template"](item)
            print("Execution TypeQL Query: "+typeql_insert_query)
            transaction.query.insert(typeql_insert_query)
            transaction.commit()

    print("\Insertion de " + str(len(items)) + " elements depuis ["+input["data_path"]+"] dans TypeDB.\n")

def build_agence_voyage_graph(inputs):
    with TypeDB.core_driver("localhost:1729") as client:
        with client.session("agence-de-voyage", SessionType.DATA) as session:
            for input in inputs:
                print("Chargement depuis ["+input["data_path"]+"] dans TypeDB ...")
                load_data_into_typedb(input, session)

inputs = [
    {
        "data_path": "Hotels",
        "template": hotel_template
    },
    {
        "data_path": "Restaurants",
        "template": restaurant_template
    },
    {
        "data_path": "Proximite",
        "template": proximite_template
    }
]

build_agence_voyage_graph(inputs)