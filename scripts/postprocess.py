from typing import Union
import numpy as np
import pandas as pd
import pendulum


def convert_datetime(x: str) -> Union[str, float]:
    """
    Convert datetime string to datetime object.
    """
    if pd.isna(x) or x == "None":
        return np.nan
    else:
        val = int(x) / 1000
        dt = pendulum.from_timestamp(val)
        dt_string = dt.to_datetime_string()
        return dt_string


if __name__ == "__main__":
    df = pd.read_json("data/geocoded_records.jsonl", lines=True)
    df.drop_duplicates(inplace=True)
    df.loc[:, "death_datetime"] = df.DeathDate.apply(convert_datetime)  # type: ignore
    # this is a bit of a hack, but it works
    df.loc[:, "death_date"] = df.DeathDate.apply(convert_datetime).apply(
        lambda x: x.split(" ")[0] if pd.notna(x) else np.nan
    )  # type: ignore
    df.to_csv("data/records.csv", index=False)
