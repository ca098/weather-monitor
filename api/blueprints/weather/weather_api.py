from flasgger import swag_from
from flask import Blueprint, jsonify, request

from services.service_engine import ServiceEngine
from utils.utils import INVALID_EMAIL_MESSAGE, HttpStatus, is_valid_email

WEATHER_BLUEPRINT = Blueprint("weather_blueprint", __name__)

SE = ServiceEngine()

# Run the email service
SE.email_service.run_mail_service()


@WEATHER_BLUEPRINT.route(
    "/api/v1/create_subscription/<string:email>/<string:location>", methods=["POST"]
)
@swag_from("swagger/create_subscription.yml")
def create_new_subscription(email: str, location: str):
    if not is_valid_email(email):
        return jsonify({"message": INVALID_EMAIL_MESSAGE}), HttpStatus.BAD_REQUEST.value
    req = request.json
    create_subscription = SE.weather_service.create_new_subscription(
        email=email, location=location.lower(), params=req
    )
    if "error" in create_subscription:
        return jsonify(create_subscription), HttpStatus.BAD_REQUEST.value
    return jsonify(create_subscription), HttpStatus.CREATED.value


@WEATHER_BLUEPRINT.route(
    "/api/v1/update_subscription/<string:email>/<string:location>", methods=["POST"]
)
@swag_from("swagger/update_subscription.yml")
def update_subscriptions(email: str, location: str):
    if not is_valid_email(email):
        return jsonify({"message": INVALID_EMAIL_MESSAGE}), HttpStatus.BAD_REQUEST.value

    req = request.json
    update_subscription = SE.weather_service.update_subscription(
        email=email, location=location.lower(), params=req
    )
    if "error" in update_subscription:
        return jsonify(update_subscription), HttpStatus.NOT_FOUND.value
    return jsonify(update_subscription), HttpStatus.OKAY.value


@WEATHER_BLUEPRINT.route("/api/v1/list_subscription/<string:email>", methods=["GET"])
@swag_from("swagger/list_subscription.yml")
def list_subscriptions(email: str):
    if not is_valid_email(email):
        return jsonify({"message": INVALID_EMAIL_MESSAGE}), HttpStatus.BAD_REQUEST.value
    return (
        jsonify(SE.weather_service.get_subscription_list(email)),
        HttpStatus.OKAY.value,
    )


@WEATHER_BLUEPRINT.route("/api/v1/get_weather_codes", methods=["GET"])
@swag_from("swagger/get_weather_codes.yml")
def get_weather_codes():
    return jsonify(SE.weather_service.get_weather_codes())


@WEATHER_BLUEPRINT.route(
    "/api/v1/delete_subscription/<string:email>/<string:location>", methods=["DELETE"]
)
@swag_from("swagger/delete_subscription.yml")
def delete_subscriptions(email: str, location: str):
    if not is_valid_email(email):
        return jsonify({"message": INVALID_EMAIL_MESSAGE}), HttpStatus.BAD_REQUEST.value
    removed_subscription = SE.weather_service.delete_subscription(
        email=email, location=location.lower()
    )
    if "error" in removed_subscription:
        return jsonify(removed_subscription), HttpStatus.NOT_FOUND.value
    return jsonify(removed_subscription), HttpStatus.OKAY.value
