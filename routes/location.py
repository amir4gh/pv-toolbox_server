from flask import Blueprint, request, jsonify
from services.location_service import get_lat_lon

location_bp = Blueprint("location", __name__)


@location_bp.route("/location", methods=["GET"])
def get_location():
    """API route to get latitude & longitude from city & country."""

    city = request.args.get("city", type=str)
    country = request.args.get("country", type=str)

    if not city or not country:
        return jsonify({"error": "Missing parameters. Provide city and country."}), 400

    result = get_lat_lon(city, country)
    return jsonify(result)
