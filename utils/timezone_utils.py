from timezonefinder import TimezoneFinder


def get_timezone(lat, lon):
    """Find timezone based on latitude and longitude."""
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lon, lat=lat)
