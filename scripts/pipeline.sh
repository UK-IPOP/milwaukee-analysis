#! /usr/bin/env bash

echo "Fetching data..."
# poetry run python scripts/fetch_data.py
echo "------------"

echo "Geocoding data..."
poetry run python scripts/geocode.py
echo "------------"

echo "Converting jsonlines to csv..."
poetry run python scripts/postprocess.py

echo "Running drug extraction tool..."
de-workflow \
    execute \
    --algorithm="osa" \
    data/records.csv \
    "CaseNum" \
    "combined_causes" 

echo "Moving drug files..."
mv report.html data/drug_report.html
mv merged_results.csv data/merged_results.csv
mv dense_results.csv data/dense_results.csv

echo "Generating pandas report..."
pandas_profiling data/records.csv data/pandas_report.html --title "Milwaukee Data Report"


echo "Copying files to OneDrive..."
cp data/drug_report.html ~/OneDrive\ -\ University\ of\ Kentucky/Data\ Stuff/Milwaukee\ Data/
cp data/merged_results.csv ~/OneDrive\ -\ University\ of\ Kentucky/Data\ Stuff/Milwaukee\ Data/
cp data/dense_results.csv ~/OneDrive\ -\ University\ of\ Kentucky/Data\ Stuff/Milwaukee\ Data/
cp data/pandas_report.html ~/OneDrive\ -\ University\ of\ Kentucky/Data\ Stuff/Milwaukee\ Data/

echo "------------"
echo "DONE! 😃"
