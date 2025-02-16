import requests


class CoinsService:
    API_URL = "https://api.data.gov.sg/v1/environment/air-temperature"

    @staticmethod
    def get_air_temperature():
        try:
            response = requests.get(CoinsService.API_URL)
            if response.status_code == 200:
                data = response.json()
                stations = {station["id"]: station for station in data["metadata"]["stations"]}
                readings = data["items"][0]["readings"]
                result = [
                    {
                        "name": stations[reading["station_id"]]["name"],
                        "latitude": stations[reading["station_id"]]["location"]["latitude"],
                        "longitude": stations[reading["station_id"]]["location"]["longitude"],
                        "temperature": reading["value"],
                        "unit": data["metadata"]["reading_unit"]
                    }
                    for reading in readings
                ]
                return result
            else:
                return {"error": "Failed to fetch data"}
        except Exception as e:
            return {"error": str(e)}
