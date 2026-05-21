# CLI Weather App 🌦️

A simple Python Command Line Interface (CLI) application that fetches real-time weather data using the WeatherAPI.

---

## Features

- Fetch real-time weather data
- Search weather by city name
- Uses environment variables for API security
- Saves API response to JSON file
- Beginner-friendly project
- Built using Python and Requests

---

## Technologies Used

- Python
- Requests
- JSON
- python-dotenv
- WeatherAPI

---

## Setup API Key

Create a `.env` file in the root directory.

Add:

```env
W_API=your_api_key_here
```

Get your API key from:

https://www.weatherapi.com/

---

## Run the Project

```bash
python main.py
```

---

## Example Output

```bash
---------------------------------------- Weather Report ----------------------------------------

Enter city name: Delhi

Weather Details
--------------------------------------------------

City: Delhi
Country: India
Temperature: 34°C
Condition: Sunny
Humidity: 60%
Wind Speed: 12 kph
```

---

## API Used

WeatherAPI

Endpoint used:

```bash
/current.json
```

Example request:

```bash
http://api.weatherapi.com/v1/current.json?key=API_KEY&q=Delhi
```

---

## Future Improvements

- Async weather fetching using `httpx`
- Multiple city support
- Better CLI UI
- Error handling improvements
- Colored terminal output
- 5-day weather forecast
- News integration

---

## Learning Outcomes

This project helped in learning:

- HTTP Requests
- API Handling
- JSON Parsing
- Environment Variables
- File Handling
- CLI Application Development

---

## Author

Yashvardhan Gupta  
BTech AI, IIT Gandhinagar