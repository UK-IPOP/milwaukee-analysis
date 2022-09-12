# Analyses for Milwaukee, WI Open Data

> This has been moved to [https://github.com/UK-IPOP/open-data-pipeline](https://github.com/UK-IPOP/open-data-pipeline)

## Description

Original site can be found [here](https://county.milwaukee.gov/EN/Medical-Examiner/Public-Data).

This replicates (in a smaller way) [previous analyses](https://github.com/UK-IPOP/geocoding) done in Chicago by extracting Open Data, geocoding, and running the drug extraction [tool](https://github.com/UK-IPOP/drug-extraction).

## Requirements

This project requires:

|                 Name                 |    Version     |
| :----------------------------------: | :------------: |
|  [python](https://www.python.org/)   | >= 3.9, < 3.10 |
| [poetry](https://python-poetry.org/) |      1.1       |
|        [Go](https://go.dev/)         |      1.17      |
| [jq](https://stedolan.github.io/jq/) |      1.6       |
|     [git](https://git-scm.com/)      |      Any       |

If you don't plan on using the drug extraction tool you will not need Go or jq.

## Usage

### Installation

`git clone` or `gh repo clone` will work to download the source code.

For example:
`git clone https://github.com/UK-IPOP/milwaukee-analysis.git`

Then `cd milwaukee-data` to move into the directory.

### Running

To run the analysis you can then simply run:

`bash scripts/pipeline.sh` inside the milwaukee-data folder.

This will fetch the data from the web (~5 minutes), geocode it (~45 minutes), perform some simple data cleaning and then download and run the drug extraction tool (a few minutes).

Your results will be in `data/results.csv` (for records) and `data/drug_results.csv` (for drug info).

Enjoy! 😁
