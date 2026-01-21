import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import time

def fetch_weather_for_city(lat, lon, start_date, end_date):
    """
    Fetches hourly historical weather data for a specific location.
    """
    # 1. Setup API Client with Caching & Retry logic
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # 2. Define API Parameters
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "boundary_layer_height"]
    }

    try:
        # 3. Call API
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # 4. Process Data
        hourly = response.Hourly()
        hourly_data = {
            "Date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "Temperature": hourly.Variables(0).ValuesAsNumpy(),
            "Humidity": hourly.Variables(1).ValuesAsNumpy(),
            "Wind_Speed": hourly.Variables(2).ValuesAsNumpy(),
            "PBLH": hourly.Variables(3).ValuesAsNumpy() # Planetary Boundary Layer Height
        }

        weather_df = pd.DataFrame(data=hourly_data)
        
        # Remove timezone info to match Kaggle dataset format
        weather_df['Date'] = weather_df['Date'].dt.tz_localize(None)
        return weather_df

    except Exception as e:
        print(f"Error fetching data for {lat}, {lon}: {e}")
        return pd.DataFrame() # Return empty if fails