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
    # Load the dataset
    df = pd.read_csv("../vispubdata-update/vispubdata-update.csv", keep_default_na=False)
    df["doi"] = df["DOI"].apply(lambda x: str(x).lower())

    # Load the matching data
    match = pd.read_csv("results/exact_matching.csv")
    non_match = df[~df['doi'].isin(match['vispub_doi'])]
    print("Non-match", non_match.shape[0])

    # All titles in AMiner dataset
    with open('results/aminer_titles.p', 'rb') as fp:
        choices = pickle.load(fp)
    print("AMiner titles", len(choices))

    start_time = time.perf_counter()
    with multiprocessing.Pool(5) as pool:
        rows = non_match.to_dict('records')
        processes = [pool.apply_async(task, args=(row,choices,)) for row in rows]
        results = [p.get() for p in processes]
    finish_time = time.perf_counter()
    print(f"Program finished in {(finish_time-start_time)/3600:.2f} hours")
    
    results = pd.DataFrame(results, columns = ["vispub_doi", "vispub_title", "aminer_id", "aminer_title", "score"])
    results.to_csv('results/candidate_papers.csv', index=False)