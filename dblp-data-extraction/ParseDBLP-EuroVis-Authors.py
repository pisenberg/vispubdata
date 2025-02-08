# # DBLP EuroVis 2008-2024 Full Paper Parser
# 
# This code extracts papers and their deduped authors from DBLP. 
# 
# To run this code first do the following:
# 
# - Go to the DBLP website https://dblp.org/xml/
# - Download the latest .xml and .dtd and put them into the **data** subfolder folder of the dblp-data-extraction folder in this repository.
# - Also update the following file in the **data** folder if needed: https://github.com/tobiasisenberg/Visualization-Reproducibility/blob/main/input/eurovis.csv
# 
# 
# This code is inspired by https://github.com/26hzhang/DBLPParser/blob/master/src/dblp_parser.py, a DBLP parser by ZHANG HAO.
# It was implemented with help and code from Tobias Isenberg and Jean-Daniel Fekete


# ## 1) Import what we need


from lxml import etree
import re
import csv
import codecs
from tqdm import tqdm
from time import sleep
import pandas as pd
import ujson
import gzip

# all of the element types in dblp
all_elements = {"article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www"}
# all of the feature types in dblp
all_features = {"address", "author", "booktitle", "cdrom", "chapter", "cite", "crossref", "editor", "ee", "isbn",
                "journal", "month", "note", "number", "pages", "publisher", "school", "series", "title", "url",
                "volume", "year"}


# ### EuroVis papers
# to identify EuroVis papers, we parse a list of EuroVis full paper DOIs because there seems to be no better way to identify them in Computer Graphics forum. Of course it would be good if this list was up to date (see link above).
# read the dois of the proper EuroVis papers (as xlsx file) - code from Tobias Isenberg

euroVisPaperDois = []
euroVisPaperMostRecentYear = 0
with pd.ExcelFile('data/EuroVisFull_CGF.xlsx') as xls:
    sheetX = xls.parse(0) # select the first sheet
    targetCellName = 'dc.identifier.doi[]'
    numberOfRows = len(sheetX[targetCellName])
    for i in range(0, numberOfRows):
        doi = sheetX[targetCellName][i]
        year = int(sheetX['dc.date.issued[en_US]'][i])
        abstract = str(sheetX['dc.description.abstract[en_US]'][i])
        if (len(abstract) > 0) and (abstract != 'nan'): # avoid including frontmatter that has no abstract
            if ((type(doi) == str) and (doi != 0) and (doi != '')): euroVisPaperDois.append(doi)
            else:
                doi = sheetX['dc.identifier.uri[en_US]'][i].replace('http://dx.doi.org/', '')
                if ((not 'handle' in doi) and ('10.1111/' in doi)):
                    euroVisPaperDois.append(doi.lower())
                # else: # this is just for double-checking, could be added to a verbose mode
                #     print('Incorrect EuroVis DOI: ' + doi)
            if (year > euroVisPaperMostRecentYear): euroVisPaperMostRecentYear = year
                
# for 2024 and onward, we just use the bibtex export from the EG DL, converted to CSV
with open('data/eurovis.csv', 'r', encoding="utf-8") as csvfile:
    # create a CSV reader object
    reader = csv.DictReader(csvfile)
    # iterate over the rows
    for row in reader:
        euroVisPaperDois.append(row['doi'].lower())
        year = int(row['year'])
        if (year > euroVisPaperMostRecentYear): euroVisPaperMostRecentYear = year
            
################## BELOW HERE IS THE CODE THAT FAILS          


# ## 2) Helper methods

def context_iter(source):
    if source.endswith(".gz"):
        source=gzip.open(source)
    ## Create a dblp data iterator of (event, element) pairs for processing
    return etree.iterparse(source=source, dtd_validation=False, load_dtd=True)  # requires the dtd 

def clear_element(element):
    ## Free up memory for temporary element tree after processing the element
    element.clear()
    while element.getprevious() is not None:
        del element.getparent()[0]

def extract_feature(elem, features, include_key=False):
    ## Extract the value of each feature
    if include_key:
        attribs = {'key': [elem.attrib['key']]}
    else:
        attribs = {}
    for feature in features:
        attribs[feature] = []
    for sub in elem:
        if sub.tag not in features:
            continue
        if sub.tag == 'title':
            text = re.sub("<.*?>", "", etree.tostring(sub).decode('utf-8')) if sub.text is None else sub.text
        else:
            text = sub.text
        if text is not None and len(text) > 0:
            attribs[sub.tag] = attribs.get(sub.tag) + [text]
    return attribs


def is_eurovis_publication(key, publications_to_search):
    ## checks if the paper has a EuroVis DOI
    key = key.lower()  # Convert text to lowercase to ensure case-insensitive search
    for publication in publications_to_search:
        if publication in key:
            return True
    return False


def parse_entity(dblp_path, save_path, type_name, features=None, save_to_csv=False, include_key=False):
    ## Parse specific elements according to the given type name and features
    ## I think this is where things break down

    print("PROCESS: Start parsing for {}...".format(str(type_name)))
    assert features is not None, "features must be assigned before parsing the dblp dataset"
    results = []
    attrib_count, full_entity, part_entity = {}, 0, 0
    pbar = tqdm(position=0, leave=True)
    
    itercount = 0
    iterstep = 100000
        
    for _, elem in context_iter(dblp_path):
    
        if itercount >= iterstep:
            sleep(0.1)
            pbar.update(iterstep)
            itercount = 0
        itercount = itercount + 1
        
        
        if elem.tag in type_name:
            attrib_values = extract_feature(elem, features, include_key)  # extract required features
            visconferences = ['vissym','journals/cgf']
            
            key = attrib_values['key'][0]
            isMaybeEuroVisPaper = is_eurovis_publication(key, visconferences)
            
            if isMaybeEuroVisPaper:
            
                addPaper = True

                if 'journals/cgf' in key:
                    #for journal papers we check if the DOI is in the list of EuroVis papers we have (because cgf published many non-EuroVis papers) 
                    # all vissym papers we add by defaul, hoping that there were never any short papers in there             
                    
                    if (not attrib_values['ee'] is None):
                        if (len(attrib_values['ee']) > 0):
                            doi = attrib_values['ee'][0].strip()
                            if len(doi) == 0:
                                addPaper = False
                            elif not doi.lower() in euroVisPaperDois:
                                addPaper = False
                        else:
                            addPaper = False
                    else:
                        addPaper = False
                
                if addPaper:
                
                    results.append(attrib_values)  # add record to results array
                    for key, value in attrib_values.items():
                        attrib_count[key] = attrib_count.get(key, 0) + len(value)
                    cnt = sum([1 if len(x) > 0 else 0 for x in list(attrib_values.values())])
                    if cnt == len(features):
                        full_entity += 1
                    else:
                        part_entity += 1
        elif elem.tag not in all_elements:
            continue
            
        clear_element(elem)
        
        
    if save_to_csv:
        f = open(save_path, 'w', newline='', encoding='utf8')
        writer = csv.writer(f, delimiter=',')
        if include_key:
            features.insert(0,'key')
            writer.writerow(features)  # write title
        else:
            writer.writerow(features)  # write title
        for record in results:
            # some features contain multiple values (e.g.: author), concatenate with `::`
            row = ['::'.join(v) for v in list(record.values())]
            writer.writerow(row)
        f.close()
    else:  # default save to json file
        with codecs.open(save_path, mode='w', encoding='utf8', errors='ignore') as f:
            ujson.dump(results, f)
    return full_entity, part_entity, attrib_count


def parse_article(dblp_path, save_path, save_to_csv=False, include_key=True):
    type_name = ['article','inproceedings']
    features = ['title', 'author', 'year', 'ee'] #ee is the doi
    info = parse_entity(dblp_path, save_path, type_name, features, save_to_csv=save_to_csv, include_key=include_key)
    print('Total articles found: {}, articles contain all features: {}, articles contain part of features: {}'
            .format(info[0] + info[1], info[0], info[1]))
    print("Features information: {}".format(str(info[2])))
    
    

dblp_path = 'data/dblp.xml.gz'
save_path = 'data/EuroVis-author-articles.csv'
try:
    context_iter(dblp_path)
    print("LOG: Successfully loaded \"{}\".".format(dblp_path))
except IOError:
    print("ERROR: Failed to load file \"{}\". Please check your XML and DTD files.".format(dblp_path))
    
parse_article(dblp_path, save_path, save_to_csv=True)
print("DONE")


