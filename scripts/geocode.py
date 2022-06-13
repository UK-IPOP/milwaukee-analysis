from __future__ import annotations
from collections import defaultdict
import json

import os

import dotenv
from arcgis.geocoding import geocode
from arcgis.gis import GIS
from tqdm import tqdm
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
    try:
        geocoded_info = geocode(
            address["combined_address"],
            search_extent=search_bounds,
            location_type="rooftop",
        )
    except:
        print(f"Failed to geocode {address['combined_address']}")
        return address
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


def remove_duplicates() -> int:
    """Removes duplicate records.

    Gets number of lines in scraped data file for progress bar.

    Returns:
        int: Number of lines in file.
        dict
    """
    data = defaultdict(dict)
    with open("data/mil_scraped.jsonl", "r") as f:
        for line in f:
            info: dict[str, str] = json.loads(line)
            cleaned = {k: v for k, v in info.items() if v != " " and v != "" and v}
            unwanted_fields = {"XCoordinate", "YCoordinate", "CaseNum_STR", "ESRI_OID"}
            cleaned = dict()
            for k, v in info.items():
                if k in unwanted_fields:
                    continue
                str_val = str(v).strip()
                if str_val and str_val != "":  # not none and not empty str
                    cleaned[k.strip()] = str_val
            data[cleaned["CaseNum"]].update(cleaned)
            data[cleaned["CaseNum"]].update(cleaned)

    count = 0
    with open("data/no_duplicates.jsonl", "w") as f:
        for _, v in data.items():
            json_data = json.dumps(v) + "\n"
            count += 1
            f.write(json_data)

    return count


def clean_data() -> list[dict[str, str]]:
    """Read data from file and generate some new composite fields.

    Yields:
        dict: A record with the new composite/cleaned fields.
    """
    data = []
    with open("data/no_duplicates.jsonl", "r") as file:
        for line in file:
            info: dict[str, str] = json.loads(line)
            address = info.get("EventAddr", "").strip()
            city = info.get("EventCity", "").strip()
            state = info.get("EventState", "").strip()
            zip_code = info.get("EventZip", "").strip()
            combined_address = f"{address}, {city}, {state} {zip_code}"
            info["combined_address"] = combined_address
            causea = info.get("CauseA", "").strip()
            causeb = info.get("CauseB", "").strip()
            cause_other = info.get("CauseOther", "").strip()
            combined_causes = f"{causea}, {causeb}, {cause_other}"
            info["combined_causes"] = combined_causes
            data.append(info)
    return data


def main():
    """Runs the geocoding."""
    _ = remove_duplicates()
    data = clean_data()
    with open("data/geocoded_records.jsonl", "w") as f:
        for record in tqdm(data):
            result = run_geocoding(record)
            json_data = json.dumps(result) + "\n"
            f.write(json_data)


if __name__ == "__main__":
    initialize()
    main()
    print("Done!")
