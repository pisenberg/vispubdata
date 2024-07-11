import pandas as pd
import json
import re
import pickle
import multiprocessing
import time

from thefuzz import fuzz
from thefuzz import process

def task(row, choices):
    #print(row['Title'])
    check = row['Title'].lower()
    match, score = process.extractOne(check, choices.keys(), scorer=fuzz.token_sort_ratio)
    print(f"{row['Title']}\n{match} | {score}")
    return [row["DOI"], row["Title"], choices[match], match, score]

if __name__ == "__main__":

    datasets = ['./vispubdata-update/results/vispubdata-update.csv',
            './vispubdata-update/results/vispubdata-update-journals.csv']
    appendices = ['vis-papers','journal-papers']


    datasets_dfs = []

    for dataset in datasets:
        df = pd.read_csv(dataset, keep_default_na=False)
        datasets_dfs.append(df)

    index = 0
    for df in datasets:


        # Load the dataset
        df = pd.read_csv(datasets[index], keep_default_na=False)
        df["doi"] = df["DOI"].apply(lambda x: str(x).lower())

        # Load the matching data
        match = pd.read_csv("./aminer-citation-update/results/exact_matching"+appendices[index]+".csv")
        non_match = df[~df['doi'].isin(match['vispub_doi'])]
        print("Non-match", non_match.shape[0])

        # All titles in AMiner dataset
        with open('./aminer-citation-update/results/aminer_titles'+appendices[index]+'.p', 'rb') as fp:
            choices = pickle.load(fp)
        print("AMiner titles", len(choices))

        start_time = time.perf_counter()
        with multiprocessing.Pool(5) as pool:
            rows = non_match.to_dict('records')
            processes = [pool.apply_async(task, args=(row,choices,)) for row in rows]
            results = [p.get() for p in processes]
        finish_time = time.perf_counter()
        print(f"Program finished in {(finish_time-start_time)/3600:.2f} hours")
        print("########################################")
        results = pd.DataFrame(results, columns = ["vispub_doi", "vispub_title", "aminer_id", "aminer_title", "score"])
        results.to_csv('./aminer-citation-update/results/candidate_papers'+appendices[index]+'.csv', index=False)
        index = index + 1