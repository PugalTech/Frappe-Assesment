import requests
import frappe

@frappe.whitelist()
def fetch_weather_data(city):
    api_key = "ad7655c98b61e90c45d61671111f159d"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "response_json": data 
        }
    else:
        frappe.throw("Failed to fetch weather data.")
