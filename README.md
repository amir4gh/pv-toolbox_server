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

[GET]/time?latitude=48.8566&longitude=2.3522
{
"current_date": "2025-03-16",
"current_time": "08:32:03",
"latitude": 48.8566,
"longitude": 2.3522,
"timezone": "Europe/Paris"
}

[GET]/solar-v2?latitude=48.8566&longitude=2.3522&date=2024-03-15
{
"average_daily_radiance": 176.62,
"date": "2024-03-15",
"hourly_radiance": {
"00:00": 0,
"01:00": 0,
"02:00": 0,
"03:00": 0,
"04:00": 0,
"05:00": 0,
"06:00": 0,
"07:00": 0,
"08:00": 77.12,
"09:00": 240.81,
"10:00": 393.8,
"11:00": 513.67,
"12:00": 589.49,
"13:00": 615.21,
"14:00": 588.89,
"15:00": 512.55,
"16:00": 392.32,
"17:00": 239.2,
"18:00": 75.84,
"19:00": 0,
"20:00": 0,
"21:00": 0,
"22:00": 0,
"23:00": 0
},
"latitude": 48.8566,
"longitude": 2.3522,
"sunrise": "13:00:00",
"sunset": "01:00:00",
"timezone": "Europe/Paris"
}

# chatgpt session:

https://chatgpt.com/share/67d6812a-e13c-8001-a433-64c99c579377
