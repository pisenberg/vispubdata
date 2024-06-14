#!/usr/bin/python3

from urllib.request import urlopen
import os,sys
import pandas as pd
import altair as alt
import csv
from math import nan
import math

#####################################
# overall settings
#####################################
inputfilename = "vispubdata.csv"
journalpresentationsfilename = "vis-journal-presentations.csv"
outputfilename = "reproducibility.pdf"
googleSheetsLocation = "https://docs.google.com/spreadsheets/d/1xgoOPu28dQSSGPIp_HHQs0uvvcyLNdkMF9XtRajhhxU/edit?usp=sharing"
googleSheetsLocation2 = "https://docs.google.com/spreadsheets/d/1I6n4a6xvmoanAIDiSsGlaOVljAJ5IkT2C_naI-dStNo/edit?usp=sharing"
visPadding = 5

#####################################
# change to directory of the script
#####################################
pathOfTheScript = os.path.dirname(sys.argv[0])
if pathOfTheScript != "": os.chdir(pathOfTheScript)

#####################################
# main parts of the script
#####################################

# check if the needed data file exists
if (os.path.isfile(inputfilename)):
    vispubdataList = []
    journalpresentationsList = []
    # load the previously downloaded data file
    with open(inputfilename, 'r', encoding="utf-8") as csvfile:
        # create a CSV reader object
        reader = csv.DictReader(csvfile)
        # iterate over the rows
        for row in reader:
            dataItem = {}
            dataItem['doi'] = row['DOI'].lower()
            dataItem['year'] = int(row['Year'])
            dataItem['papertype'] = row['PaperType']
            dataItem['venue'] = row['Conference']

            if dataItem['papertype'] in ['C', 'J']:
                vispubdataList.append(dataItem)
    
    if (os.path.isfile(journalpresentationsfilename)):
        with open(journalpresentationsfilename, 'r', encoding="utf-8") as csvfile:
            # create a CSV reader object
            reader = csv.DictReader(csvfile)
            # iterate over the rows
            for row in reader:
                dataItem = {}
                dataItem['doi'] = row['doi'].lower()
                dataItem['year'] = int(row['year'])
                dataItem['journal'] = row['journal']
                journalpresentationsList.append(dataItem)
    else:
        print("The input data file " + journalpresentationsfilename + " was not found, please first go the shared Google Sheets location.")
        print("There download the journal presentations dataset as a CSV file to " + journalpresentationsfilename + ". The url for the data is:")
        print(googleSheetsLocation2)

    # find first and last year of the dataset, and all venues
    listOfVenuesToShow = ["VIS/VisWeek incl. TVCG/CG&A", "VIS/VisWeek w/o TVCG/CG&A", "Vis (1990-2011)", "SciVis (2012 onward)", "VAST", "InfoVis", "SciVis conf.", "VAST conf.", "TVCG @ VIS", "CG&A @ VIS"]
    firstYear = vispubdataList[0]['year']
    lastYear = vispubdataList[0]['year']
    listOfVenuesInData = []
    for item in vispubdataList:
        if item['year'] < firstYear: firstYear = item['year']
        if item['year'] > lastYear: lastYear = item['year']
        if not item['venue'] in listOfVenuesInData: listOfVenuesInData.append(item['venue'])
    # print(listOfVenuesInData) # ['Vis', 'VAST', 'InfoVis', 'SciVis']
    # lastYear = 2023 # FIXME: just for testing

    # create the empty dataset, still with the original venue names
    visPubDataAggregation = {}
    for venue in listOfVenuesInData + ['TVCG', 'CG&A']:
        visPubDataAggregation[venue + "-C"] = {}
        visPubDataAggregation[venue + "-J"] = {}
        for year in range(firstYear, lastYear + 1):
            visPubDataAggregation[venue + "-C"][year] = nan
            visPubDataAggregation[venue + "-J"][year] = nan

    # fill the aggregated data with entries from the list, still with the original venue names
    for item in vispubdataList:
        year = item['year']
        venue = item['venue']
        type = item['papertype']
        if math.isnan(visPubDataAggregation[venue + "-" + type][year]): visPubDataAggregation[venue + "-" + type][year] = 1
        else: visPubDataAggregation[venue + "-" + type][year] += 1

    # add the journal presentation data
    for item in journalpresentationsList:
        year = item['year']
        journal = item['journal']
        if math.isnan(visPubDataAggregation[journal + "-J"][year]): visPubDataAggregation[journal + "-J"][year] = 1
        else: visPubDataAggregation[journal + "-J"][year] += 1

    # now let's transfer the data to the more complex scheme, starting with the empty set
    visPubDataAggregationDetailed = {}
    for venue in listOfVenuesToShow:
        visPubDataAggregationDetailed[venue] = {}
        for year in range(firstYear, lastYear + 1):
            visPubDataAggregationDetailed[venue][year] = nan
    
    # this needs some background info on naming and years
    # first, the original Vis conference, from 1990 to 2011 (inclusive); up to 2005 they were conference papers
    for year in range(firstYear, 2006): visPubDataAggregationDetailed[listOfVenuesToShow[2]][year] = visPubDataAggregation['Vis-C'][year]
    for year in range(2006, 2012): visPubDataAggregationDetailed[listOfVenuesToShow[2]][year] = visPubDataAggregation['Vis-J'][year]
    # then the (renamed) SciVis conference, technically from 2012 but since we want to connect the lines we start from 2011
    visPubDataAggregationDetailed[listOfVenuesToShow[3]][2011] = visPubDataAggregation['Vis-J'][2011]
    for year in range(2012, lastYear + 1): visPubDataAggregationDetailed[listOfVenuesToShow[3]][year] = visPubDataAggregation['SciVis-J'][year]
    # InfoVis is easy; up to 2005 as conference, then as journal
    for year in range(firstYear, 2006): visPubDataAggregationDetailed[listOfVenuesToShow[5]][year] = visPubDataAggregation['InfoVis-C'][year]
    for year in range(2006, lastYear + 1): visPubDataAggregationDetailed[listOfVenuesToShow[5]][year] = visPubDataAggregation['InfoVis-J'][year]
    # so is VAST; up to 2012 as conference, then as journal
    for year in range(firstYear, 2013): visPubDataAggregationDetailed[listOfVenuesToShow[4]][year] = visPubDataAggregation['VAST-C'][year]
    for year in range(2013, lastYear + 1): visPubDataAggregationDetailed[listOfVenuesToShow[4]][year] = visPubDataAggregation['VAST-J'][year]
    # VAST conference from 2014 on
    for year in range(2014, lastYear + 1): visPubDataAggregationDetailed[listOfVenuesToShow[7]][year] = visPubDataAggregation['VAST-C'][year]
    # SciVis conference only in 2015
    visPubDataAggregationDetailed[listOfVenuesToShow[6]][2015] = visPubDataAggregation['SciVis-C'][2015]
    # TVCG journal presentations
    for year in range(firstYear, lastYear + 1): visPubDataAggregationDetailed[listOfVenuesToShow[8]][year] = visPubDataAggregation['TVCG-J'][year]
    # CG&A journal presentations
    for year in range(firstYear, lastYear + 1): visPubDataAggregationDetailed[listOfVenuesToShow[9]][year] = visPubDataAggregation['CG&A-J'][year]

    # finally, sum up the totals
    for year in range(firstYear, lastYear + 1):
        sum = 0
        # for venue in listOfVenuesToShow[2:6]: # we do not include the later conference-only papers
        for venue in listOfVenuesToShow[2:8]:
            if not math.isnan(visPubDataAggregationDetailed[venue][year]):
                sum += visPubDataAggregationDetailed[venue][year]
        visPubDataAggregationDetailed[listOfVenuesToShow[1]][year] = sum
        sum = 0
        # for venue in listOfVenuesToShow[2:6]: # we do not include the later conference-only papers
        #     if not math.isnan(visPubDataAggregationDetailed[venue][year]):
        #         sum += visPubDataAggregationDetailed[venue][year]
        # for venue in listOfVenuesToShow[9:10]: # but here the journal presentations
        #     if not math.isnan(visPubDataAggregationDetailed[venue][year]):
        #         sum += visPubDataAggregationDetailed[venue][year]
        for venue in listOfVenuesToShow[2:10]:
            if not math.isnan(visPubDataAggregationDetailed[venue][year]):
                sum += visPubDataAggregationDetailed[venue][year]
        visPubDataAggregationDetailed[listOfVenuesToShow[0]][year] = sum
    # but without counting Vis/SciVis 2011 twice (see hack from before):
    visPubDataAggregationDetailed[listOfVenuesToShow[1]][2011] -= visPubDataAggregationDetailed[listOfVenuesToShow[3]][2011]
    visPubDataAggregationDetailed[listOfVenuesToShow[0]][2011] -= visPubDataAggregationDetailed[listOfVenuesToShow[3]][2011]

    # and add the final unified VIS starting from 2021
    for year in range(2021, lastYear + 1):
        visPubDataAggregationDetailed[listOfVenuesToShow[1]][year] += visPubDataAggregation['Vis-J'][year]
        visPubDataAggregationDetailed[listOfVenuesToShow[0]][year] += visPubDataAggregation['Vis-J'][year]

    # empty years (should actually not be needed)
    for year in range(firstYear, lastYear + 1):
        if visPubDataAggregationDetailed[listOfVenuesToShow[1]][year] == 0: visPubDataAggregationDetailed[listOfVenuesToShow[1]][year] = nan
        if visPubDataAggregationDetailed[listOfVenuesToShow[0]][year] == 0: visPubDataAggregationDetailed[listOfVenuesToShow[0]][year] = nan

    # now for the visualization
    dataToPlot = []
    for venue in listOfVenuesToShow: # redo the data for the line graph, because this is not stacked
        for year in range(firstYear, lastYear + 1):
            dataToPlot.append({"venue": venue, "name": venue, "year": year, "count": visPubDataAggregationDetailed[venue][year]})#, "order": color_number * 2, "order2": color_number})
    altairData = pd.DataFrame(dataToPlot)
    # we need to layer the SciVis conf. data, as only that one needs to be shown with a dot
    dataToPlot2 = []
    for year in range(firstYear, lastYear + 1):
        dataToPlot2.append({"venue": venue, "name": venue, "year": year, "count": visPubDataAggregationDetailed['SciVis conf.'][year]})#, "order": color_number * 2, "order2": color_number})
    altairData2 = pd.DataFrame(dataToPlot2)

    # regular data
    chart1 = alt.Chart(altairData, width={"step": 15}).mark_line().encode(
        x = alt.X('year:N', title=None).axis(labelAngle=-45),
        y = alt.Y('count:Q', title=None),
        strokeWidth=alt.value(3),
        color = alt.Color('name:N', sort=None, title=None),
        order = alt.Order("venue:Q")
    )
    # the special treatment for SciVis conf. data
    chart2 = alt.Chart(altairData2, width={"step": 15}).mark_point(filled=True).encode(
        x = alt.X('year:N', title=None).axis(labelAngle=-45),
        y = alt.Y('count:Q', title=None),
        size=alt.value(45),
        color = alt.value('#77a2d4'),
        order = alt.Order("venue:Q")
    )
    chart = (chart1+chart2).configure_range(
        #                           l gray     d gray     orange    blue       green       red        l blue     l green   l purple   d purple
        category=alt.RangeScheme(['#aaaaaa', '#444444', '#f58518', '#4c78a8', '#54a24b', '#e45756', '#77a2d4', '#84d278', '#b279a2', '#5f2d53', '#ff9da6', '#bab0ac'])
    ).configure_legend(columns=4, orient='bottom', direction='horizontal', titleLimit=0, labelLimit=0, symbolSize=200, symbolStrokeWidth=3.5
    ).configure_view(strokeWidth=0).properties(
        padding={"left": visPadding, "right": visPadding, "bottom": visPadding, "top": visPadding},
        width=600,
        height=300
    )
    chart.save(outputfilename)

else:
    print("The input data file " + inputfilename + " was not found, please first go the shared Google Sheets location.")
    print("There download the VisPubData dataset as a CSV file to " + inputfilename + ". The url for the data is:")
    print(googleSheetsLocation)
