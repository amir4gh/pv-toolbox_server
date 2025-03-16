# pv-toolbox_server

[GET]/location?city=Paris&country=France
{
"city": "Paris",
"country": "France",
"latitude": 48.8588897,
"longitude": 2.32004102172008
}

[GET]/solar?latitude=48.8566&longitude=2.3522&date=2024-03-15
{
"date": "2024-03-15",
"irradiance_at_noon": 589.49,
"latitude": 48.8566,
"longitude": 2.3522,
"peak_sun_hours": 4.24,
"timezone": "Europe/Paris"
}

[GET]/location-v2?city=Bou%20saada&country=Algeria
{
"city": "Bou saada",
"country": "Algeria",
"current_date": "2025-03-16",
"current_time": "08:14:38",
"latitude": 35.2133123,
"longitude": 4.1809702,
"timezone": "Africa/Algiers"
}
