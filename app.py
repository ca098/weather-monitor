from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from api.blueprints.weather.weather_api import WEATHER_BLUEPRINT
from utils.logger_utils import get_api_logger
from utils.utils import API_ROOT_TEXT

app = Flask(__name__)
app.register_blueprint(WEATHER_BLUEPRINT)

template = {
  "swagger": "2.0",
  "info": {
    "title": "Weather Monitor API",
    "description": "API to subscribe to weather patterns",
    "contact": {
      "email": "cradams@hotmail.co.uk",
    },
    "version": "0.0.1"
  },
  "schemes": [
    "http"
  ],
}

LOG = get_api_logger()

CORS(app)
swagger = Swagger(app, template=template)


@app.route("/")
def root():
    return API_ROOT_TEXT


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="localhost")
    # app.run(debug=False, port=5000, host='0.0.0.0', ssl_context='adhoc', threaded=True)
