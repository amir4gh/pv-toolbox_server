from flask import Blueprint, request, jsonify
from services.location_service import get_lat_lon, get_time_for_location

location_bp = Blueprint("location", __name__)


@location_bp.route("/location", methods=["GET"])
def get_location():
    """API route to get latitude, longitude, and current date-time from city & country."""

    city = request.args.get("city", type=str)
    country = request.args.get("country", type=str)

    if not city or not country:
        return jsonify({"error": "Missing parameters. Provide city and country."}), 400

    result = get_lat_lon(city, country)
    return jsonify(result)


@location_bp.route("/time", methods=["GET"])
def get_time():
    """API route to get the current date & time for a specific latitude & longitude."""

    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)

    if latitude is None or longitude is None:
        return (
            jsonify({"error": "Missing parameters. Provide latitude and longitude."}),
            400,
        )

    result = get_time_for_location(latitude, longitude)
    return jsonify(result)
