from flask import Flask
from routes.solar import solar_bp
from routes.location import location_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(solar_bp)
app.register_blueprint(location_bp)

if __name__ == "__main__":
    from waitress import serve

    print("Starting production server...")
    serve(app, host="0.0.0.0", port=10000)
