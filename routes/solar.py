from flask import Blueprint, request, jsonify
from services.solar_service import calculate_solar_irradiance, get_solar_v2

solar_bp = Blueprint("solar", __name__)


@solar_bp.route("/solar", methods=["GET"])
def get_solar():
    """API route to get solar irradiance & PSH."""

    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    date = request.args.get("date", type=str)

    if None in [latitude, longitude, date]:
        return (
            jsonify(
                {"error": "Missing parameters. Provide latitude, longitude, and date."}
            ),
            400,
        )

    result = calculate_solar_irradiance(latitude, longitude, date)
    return jsonify(result)


@solar_bp.route("/solar-v2", methods=["GET"])
def get_solar_v2_route():
    """API route to get sunrise, sunset, hourly solar irradiance, and daily average radiance."""

    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    date = request.args.get("date", type=str)

    if None in [latitude, longitude, date]:
        return (
            jsonify(
                {"error": "Missing parameters. Provide latitude, longitude, and date."}
            ),
            400,
        )

    result = get_solar_v2(latitude, longitude, date)
    return jsonify(result)
