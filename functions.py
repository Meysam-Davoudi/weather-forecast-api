import json
import requests
from datetime import datetime, timezone
from database_handler import DatabaseHandler

db = DatabaseHandler('database.db')


def convert_unix_to_string(unix_timestamp, datetime_format="%Y-%m-%d"):
    date_obj = datetime.fromtimestamp(int(unix_timestamp), tz=timezone.utc)
    date_string = date_obj.strftime(datetime_format)

    return date_string


def get_country_list():
    db.connect()
    countries = db.select("countries")
    db.disconnect()

    result = []

    for country in countries:
        result.append(f"{country[1]}, {country[2]}")

    return result


def get_requests_history():
    db.connect()
    result = db.select("request_history")
    db.disconnect()

    return result


def get_request_json_data(id):
    db.connect()
    json_data = db.select("request_history", "response", f"id = {id}")
    db.disconnect()

    if isinstance(json_data, list) and len(json_data) > 0 and isinstance(json_data[0], tuple):
        json_data = json_data[0][0]

    return json_data


def clear_requests_history():
    db.connect()
    db.delete("request_history")
    db.disconnect()


def delete_request_history(id):
    db.connect()
    db.delete("request_history", f"id = {id}")
    db.disconnect()


def get_weather_status(location, forecast=None):
    weather_base_url = "http://api.weatherapi.com/v1/"
    weather_api_key = "942117675ec24ffe84f81348240103"

    weather_parameters = {
        "key": weather_api_key,
        "q": location
    }

    if forecast:
        weather_parameters["days"] = forecast
        weather_api_page = "forecast.json"
        request_type = f"forecast({forecast})"
    else:
        weather_api_page = "current.json"
        request_type = "current"

    response = requests.get(url=weather_base_url + weather_api_page, params=weather_parameters).json()

    if "location" in response:
        data = {
            'location': location,
            'lat_lon': f'{response["location"]["lat"]},{response["location"]["lon"]}',
            'request_type': request_type,
            'request_time': int(datetime.now().timestamp()),
            'response': json.dumps(response)
        }
        db.connect()
        db.insert('request_history', data)
        db.disconnect()

    return response


def weather_card_html_layout(weather_data=None):
    result_html_layout = ""

    if weather_data:
        for weather in weather_data:
            result_html_layout += f'''
                <div style="border: 2px solid #e6e6e6; border-radius: 5px; margin-top:30px; padding: 10px; width: 25%;
                            text-align:center; float:left">
                    <img src="{weather["image_url"]}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%;">
                    <h2 style="margin-top: 10px; margin-bottom: 5px;">{weather["temperature"]}°C</h2>
                    <p style="margin-top: 0; margin-bottom: 10px;">{weather["description"]}</p>
                    <p style="margin-top: 0; margin-bottom: 10px;">{weather["date"]}</p>
                </div>
                '''

    return result_html_layout
