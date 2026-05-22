from dotenv import load_dotenv #type: ignore
import json
import requests
import os
load_dotenv()

api_key = os.getenv("W_API")

url ="http://api.weatherapi.com/v1"


print("-"* 40,"Weather Report","-"* 40)
city = input("Enter the name of City of which you want a wheater report:")


response = requests.get(f"{url}/current.json?key={api_key}&q={city}")
data = response.json()

with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print(f"City: {data['location']['name']}")
print(f"Country: {data['location']['country']}")
print(f"Time at which the data was fetched: {data['current']['last_updated']}")
print(f"Temperature: {data['current']['temp_c']}°C")
print(f"Condition: {data['current']['condition']['text']}")
print(f"Humidity: {data['current']['humidity']}%")
print(f"Wind Speed: {data['current']['wind_kph']} kph")