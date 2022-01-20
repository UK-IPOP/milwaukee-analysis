#! /usr/bin/env bash

echo "Fetching data..."
poetry run python scripts/fetch_data.py
echo "------------"

echo "Geocoding data..."
poetry run python scripts/geocode.py
echo "------------"

# echo "Installing drug extraction tool..."
# go install github.com/UK-IPOP/drug-extraction@latest
# echo "------------"

echo "Converting jsonlines to csv..."
cat data/geocoded_records.jsonl | jq --slurp -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' > data/records.csv

echo "Running drug extraction tool..."
drug-extraction pipeline data/records.csv --target-col="combined_causes" --id-col="CaseNum" --format --format-type=csv

echo "Removing output..."
mv output.csv data/drug_results.csv
rm output.jsonl
echo "------------"

echo "DONE! 😃"