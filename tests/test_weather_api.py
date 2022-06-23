import json
import random

import pytest
from faker import Faker

from app import app  # Flask instance of the API
from services.service_engine import ServiceEngine
from tests.test_utils import *
from utils.utils import API_ROOT_TEXT

SE = ServiceEngine()
fake = Faker()


def get_valid_user_params() -> [str, str]:
    mail = fake.email()
    location = random.choice(CITIES)
    return mail, location


def get_valid_request_body() -> dict:
    return {
        "tempCelsiusAbove": random.randint(-1, 40),
        "tempCelsiusBelow": random.randint(-40, 25),
        "weatherCodeEquals": random.choice(list(SE.weather_service.get_weather_codes().values())),
        "windSpeedExceeds": random.randint(4, 40),
    }


def create_subscription(email: str, location: str, params: dict):
    return app.test_client().post(f'/api/v1/create_subscription/{email}/{location}',
                                  data=json.dumps(params), content_type='application/json')


@pytest.mark.get_request
def test_index_route():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.data.decode("utf-8") == API_ROOT_TEXT


@pytest.mark.post_request
def test_valid_create_subscription():
    email, location = get_valid_user_params()
    request_body = get_valid_request_body()

    valid_response = create_subscription(email=email, location=location, params=request_body)
    assert valid_response.status_code == 201
    assert valid_response.json == {'message': 'Subscription has been created successfully'}
