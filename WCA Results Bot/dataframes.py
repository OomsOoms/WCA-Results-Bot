import pandas as pd
import time
import requests
import zipfile

if False:
    url = "https://www.worldcubeassociation.org/results/misc/WCA_export.tsv.zip"
    print("Downloading updated data")
    response = requests.get(url)
    open("exports.zip", "wb").write(response.content)


start = time.perf_counter()

print("Loading dataframes to memory...")

# Open the ZIP file
with zipfile.ZipFile('exports.zip', 'r') as zip_ref:

    # Read the TSV file into a DataFrame
    print("Reading `WCA_export_Results.tsv`")
    results_df = pd.read_csv(zip_ref.open(
        'WCA_export_Results.tsv'), sep='\t', dtype="object")

    print("Reading `WCA_export_Persons.tsv`")
    persons_df = pd.read_csv(zip_ref.open(
        'WCA_export_Persons.tsv'), sep='\t', dtype="object")

    print("Reading `WCA_export_RanksAverage.tsv`")
    RanksAverage_df = pd.read_csv(zip_ref.open(
        'WCA_export_RanksAverage.tsv'), sep='\t', dtype="object")

    print("Reading `WCA_export_RanksSingle.tsv`")
    RanksSingle_df = pd.read_csv(zip_ref.open(
        'WCA_export_RanksSingle.tsv'), sep='\t', dtype="object")

    print("Reading `WCA_export_Events_edited.tsv`")
    Events_df = pd.read_csv(
        'WCA_export_Events_edited.tsv', sep='\t', dtype="object")

    print(round(time.perf_counter()-start, 2), "Seconds to load")
