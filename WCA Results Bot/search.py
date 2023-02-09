import time
import pandas as pd


def search_tsv(file_name, cols, values, return_data, isin_any):

    # start = time.perf_counter()

    # Read the TSV file into a Pandas DataFrame, using the '\t' delimiter
    # and the `chunksize` parameter to read the file in chunks of 650,000 rows
    chunks = pd.read_csv(f'WCA_export_{file_name}.tsv', delimiter='\t',
                         usecols=cols, dtype="object", chunksize=650_000)

    # Initialize an empty list to store the data
    if return_data:
        data_list = []

    # Initialize an empty list to store the data
    else:
        index_list = []

    # Loop through the chunks
    for chunk in chunks:
        # Use the `isin` method to check if each value is in any of the columns
        if isin_any:
            matches = chunk[cols].isin(values).all(axis=1)

        else:
            matches = chunk[cols].isin(values).any(axis=1)

        # Use boolean indexing to select only the rows that contain all of the values
        rows = chunk[matches]

        # Append the rows to the list
        if return_data:
            data_list.append(rows)

        # Append the index of the rows to the list
        else:
            index_list.extend(rows.index.tolist())

    # Concatenate the list of DataFrames into a single DataFrame
    if return_data:
        data = pd.concat(data_list)

    # Concatenate the list of indexes into a single list
    else:
        indexes = pd.Index(index_list)

    # print(f"Chunked time taken: {time.perf_counter()-start}")

    if return_data:
        return data
    else:
        return indexes


# search_tsv(file_name, columns used when reading the file, values to search for, return data or the indexes, if the value has to be equal to the row or just a)
# search = search_tsv("Persons", ["id", "subid", "name", "countryId", "gender"], ["2018NETT01"], True, False)
