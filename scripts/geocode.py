from __future__ import annotations
import json

import os
from typing import Iterable

import dotenv
from arcgis.geocoding import geocode
from arcgis.gis import GIS
from rich.progress import track
from rich import pretty, print


def initialize():
    """Initialize ArcGIS and pretty."""
    pretty.install()
    dotenv.load_dotenv()
    GIS(
        api_key=os.getenv("ARCGIS_API_KEY"),
    )


def run_geocoding(address: dict[str, str]) -> dict[str, str]:
    """Runs the geocoding for the address.

    Returns:
        geodata: Modified record with geocoded data or original record if geocoding failed.
    """
    search_bounds = {
        "xmin": -87.85,
        "ymin": 42.93,
        "xmax": -88.09,
        "ymax": 43.12,
        "spatialReference": {"wkid": 4326},
    }
    geocoded_info = geocode(
        address["combined_address"],
        search_extent=search_bounds,
        location_type="rooftop",
    )
    if geocoded_info:
        best_result = geocoded_info[0]
        geo_data = {
            "geocoded_address": best_result["address"],
            "geocoded_latitude": best_result["location"]["y"],
            "geocoded_longitude": best_result["location"]["x"],
            "geocoded_score": best_result["score"],
        }
        combined = address | geo_data
        return combined
    else:
        return address


def clean_data() -> Iterable[dict[str, str]]:
    """Read data from file and generate some new composite fields.

    Yields:
        dict: A record with the new composite/cleaned fields.
    """
    with open("data/mil_scraped.jsonl", "r") as file:
        for line in file:
            info: dict[str, str] = json.loads(line)
            address = info["EventAddr"].strip() if info["EventAddr"] else ""
            city = info["EventCity"].strip() if info["EventCity"] else ""
            state = info["EventState"].strip() if info["EventState"] else ""
            zip_code = info["EventZip"].strip() if info["EventZip"] else ""
            info["combined_address"] = f"{address} {city} {state} {zip_code}"
            causea = info["CauseA"].strip() if info["CauseA"] else ""
            causeb = info["CauseB"].strip() if info["CauseB"] else ""
            cause_other = info["CauseOther"].strip() if info["CauseOther"] else ""
            info["combined_causes"] = f"{causea} {causeb} {cause_other}"
            unwanted_fields = {"XCoordinate", "YCoordinate", "CaseNum_STR", "ESRI_OID"}
            data = dict()
            for k, v in info.items():
                if k in unwanted_fields:
                    continue
                if type(v) == str:
                    data[k.strip()] = v.strip()
                else:
                    data[k.strip()] = v
            if data["combined_address"] == "":
                yield data
            yield data


def get_file_lines() -> int:
    """Gets number of lines in scraped data file for progress bar."""
    count = 0
    with open("data/mil_scraped.jsonl", "r") as f:
        for _ in f:
            count += 1
    return count


def main():
    """Runs the geocoding."""
    file_lines = get_file_lines()
    with open("data/geocoded_records.jsonl", "w") as f:
        data = clean_data()
        for record in track(data, description="Running pipeline...", total=file_lines):
            result = run_geocoding(record)
            json_data = json.dumps(result) + "\n"
            f.write(json_data)


if __name__ == "__main__":
    initialize()
    main()
    print("Done!")
