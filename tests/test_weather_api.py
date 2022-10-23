import json
import random

import pytest
from faker import Faker

from app import app
from services.service_engine import ServiceEngine
from tests.test_utils import *
from utils.utils import API_ROOT_TEXT

SE = ServiceEngine()
fake = Faker()


def get_valid_user_params() -> [str, str]:
    mail = fake.email()
    location = random.choice(CITIES).lower()
    return mail, location


def get_valid_request_body() -> dict:
    return {
        "tempCelsiusAbove": random.randint(-1, 40),
        "tempCelsiusBelow": random.randint(-40, 25),
        "weatherCodeEquals": random.choice(
            list(SE.weather_service.get_weather_codes().values())
        ),
        "windSpeedExceeds": random.randint(4, 40),
    }


def create_or_update_subscription(email: str, location: str, params: dict, update=None):
    base_param = "create_subscription" if not update else "update_subscription"
    return app.test_client().post(
        f"/api/v1/{base_param}/{email}/{location}",
        data=json.dumps(params),
        content_type="application/json",
    )


def delete_subscription(email: str, location: str):
    return app.test_client().delete(f"/api/v1/delete_subscription/{email}/{location}")


def list_subscriptions(email: str):
    return app.test_client().get(f"/api/v1/list_subscription/{email}")


@pytest.mark.get_request
def test_index_route():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.data.decode("utf-8") == API_ROOT_TEXT


@pytest.mark.post_request
def test_create_subscription():
    email, location = get_valid_user_params()
    request_body = get_valid_request_body()

    valid_response = create_or_update_subscription(
        email=email, location=location, params=request_body, update=False
    )
    assert valid_response.status_code == 201
    assert valid_response.json == {
        "message": "Subscription has been created successfully"
    }

    already_exists_response = create_or_update_subscription(
        email=email, location=location, params=request_body, update=False
    )
    assert already_exists_response.status_code == 400
    assert already_exists_response.json == {
        "error": f"Entry already exists for the email '{email}', and location '{location}'."
        f" Please remove the entry to be able to add a new one."
    }


@pytest.mark.post_request
def test_update_subscription():
    email, location = get_valid_user_params()
    request_body = get_valid_request_body()

    initial_response = create_or_update_subscription(
        email=email, location=location, params=request_body, update=True
    )
    assert initial_response.status_code == 404
    assert initial_response.json == {
        "error": f"No subscription found for the location '{location}', and email '{email}'."
    }

    valid_response = create_or_update_subscription(
        email=email, location=location, params=request_body, update=False
    )
    assert valid_response.status_code == 201

    request_body["windSpeedExceeds"] += 1
    updated_response = create_or_update_subscription(
        email=email, location=location, params=request_body, update=True
    )
    assert updated_response.status_code == 200
    assert updated_response.json == {
        "message": "Subscription has been updated successfully"
    }


@pytest.mark.delete_request
def test_delete_subscription():
    email, location = get_valid_user_params()

    not_found_response = delete_subscription(email=email, location=location)
    assert not_found_response.status_code == 404
    assert not_found_response.json == {
        "error": f"Subscription for email '{email}' and location '{location}' was not found."
    }


@pytest.mark.get_request
def test_list_subscriptions():
    email, location = get_valid_user_params()
    request_body = get_valid_request_body()

    """
     TODO - loop over a few times and iteratively add distinct location paired with original email,
            keep record of each location and assert email is valid in list, as well as locations.
    """

    valid_response = create_or_update_subscription(
        email=email, location=location, params=request_body, update=False
    )
    assert valid_response.status_code == 201

    _, location = get_valid_user_params()
    request_body = get_valid_request_body()

    valid_response = create_or_update_subscription(
        email=email, location=location, params=request_body, update=False
    )
    assert valid_response.status_code == 201

    response = list_subscriptions(email=email)
    assert response.status_code == 200
    for resp in response.json:
        assert resp["email"] == email
