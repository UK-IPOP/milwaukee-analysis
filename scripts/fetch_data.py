import requests
import json
from rich import print


url = "https://lio.milwaukeecountywi.gov/arcgis/rest/services/MedicalExaminer/PublicDataAccess/MapServer/1/query?f=json&where=1%3D1&outFields=*&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outSR=102100"


def scrape_data(url):
    """Scrape data gets the data from the MIL web API.

    It writes the scraped data to file for later analysis.

    Args:
        url (str): Base url to scrape from.
    """
    payload = {"resultOffset": 0}
    response_valid = True

    with open("data/mil_scraped.jsonl", "w") as f:
        while response_valid:
            response = requests.get(url, params=payload)
            print(response.status_code, "--", payload["resultOffset"])
            data = response.json()
            if len(data["features"]) == 0:
                response_valid = False
                break
            for record in data["features"]:
                info = record["attributes"]
                json_info = json.dumps(info) + "\n"
                f.write(json_info)
            payload["resultOffset"] += 1000


if __name__ == "__main__":
    scrape_data(url)
    print("Done!")
