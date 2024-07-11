import pandas as pd


vispubcitationdf = pd.read_csv("./vispubdata-update/results/citations_references_vispubdata.csv", keep_default_na=False)
vispubcitationdf.citedPapersWithoutDOI = vispubcitationdf.citedPapersWithoutDOI.str.replace('\n','').str.lower()

print(vispubcitationdf.head())

# Google Sheet URL
references_url = "https://docs.google.com/spreadsheets/d/1mNkYHL0ly0TpCqYgaBP5ZvjXmRuaUwcDV6zSidNPVfI/gviz/tq?tqx=out:csv"



# Read the CSV into a DataFrame
references_df = pd.read_csv(references_url,keep_default_na=False)
references_df.title = references_df.Title.str.lower()
print(references_df.head())

paperWithReference = []
citedPaper = []



for index,row in references_df.iterrows():
    doi = row['DOI']
    title = row['Title']
    scale = row['Shortname']
    if doi == "":
        continue

    #search by DOI
    foundpapersdf = vispubcitationdf[vispubcitationdf['citedPapers'].str.contains(doi)]

    papersFoundCount = len(foundpapersdf.index)
    if(papersFoundCount > 0):
        paperWithReference.extend(foundpapersdf['DOI'].tolist())
        citedPaper.extend(papersFoundCount * [scale])

    #search by title - it would be smarter to do this with a string edit distance threshold
    foundpapersdf = vispubcitationdf[vispubcitationdf['citedPapersWithoutDOI'].str.contains(title)]

    papersFoundCount = len(foundpapersdf.index)
    if(papersFoundCount > 0):
        paperWithReference.extend(foundpapersdf['DOI'].tolist())
        citedPaper.extend(papersFoundCount * [scale])

    
citingPapers = pd.DataFrame({'CitingPaper':paperWithReference,'CitedPaper':citedPaper})

print(citingPapers.head())
citingPapers.to_csv("CitingPapers.csv",index=False)
    
  

# for index,row in vispubcitationdf.iterrows():
    
#     doi = row['DOI']
#     pubscited = row[crossRefPubsCited_column]
#     citation = row[crossRefCitation_column]

#     vispubdata_new.loc[vispubdata_new['DOI'] == doi,crossRefPubsCited_column] = pubscited
#     vispubdata_new.loc[vispubdata_new['DOI'] == doi,crossRefCitation_column] = citation



# vispubdata_new.to_csv("results/DEBUG_vispubdata_new.csv")

# vispubdata_new.head()