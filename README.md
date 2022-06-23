# Weather Monitor

This is a lightweight Flask API to create weather alerts for subscribed topics. The current metrics as an example are:
```sh
{
    "tempCelsiusAbove": 18,
    "tempCelsiusBelow": 2,
    "weatherCodeEquals": 800,
    "windSpeedExceeds": 35,
}
```

I've added an endpoint at `/api/v1/get_weather_codes` that will return the list of available weather codes. An example response is:

```sh
curl -s http://127.0.0.1:5000//api/v1/get_weather_codes

{
  "clear": 800,
  "clouds": 801,
  "drizzle": 300,
  "rain": 500,
  "snow": 600,
  "thunderstorm": 200,
  "tornado": 781
}
```

## Prerequisites

* [Python 3.9](https://www.python.org/downloads/release/python-399/)

## Getting Started

To install dependencies and start the server in development mode:

```sh
brew install redis
brew services start redis

pip install poetry
poetry install
python app.py
```

The server will now be running on an available port (defaulting to 5000).

```sh
http://127.0.0.1:5000/apidocs
```

The `local.env` file needs to be populated with suitable credentials to connect to a `mysql` database, OpenWeatherMap & OpenCage. I used AWS RDS to create a `mysql` database for this project. The security group is set to public, so if needed email me at: [cradams@hotmail.co.uk](cradams@hotmail.co.uk) and I can set you up with it.


You can run the tests with:

```sh
pytest
```

To update the environment variables locally:
```sh
make dev_export
```



