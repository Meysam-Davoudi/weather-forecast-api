import requests
from database_handler import DatabaseHandler

url = f"https://countriesnow.space/api/v0.1/countries/capital"
response = requests.get(url)
countries_json = response.json()

for key, item in enumerate(countries_json["data"]):
    if item["iso3"] == "ISR":
        del countries_json["data"][key]

db = DatabaseHandler('database.db')
db.connect()

for country in countries_json["data"]:
    # country = {'name': 'Country1', 'capital': 'Capital1', 'iso2': 'ISO2', 'iso3': 'ISO3'}
    db.insert('countries', country)

db.disconnect()
