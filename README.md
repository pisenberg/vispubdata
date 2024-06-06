# Vispubdata Update

This code will allow to create an update of the vispubdata dataset you can find here: https://sites.google.com/site/vispubdata. If you have only small fixes of the data to report you might be better off to leave a comment on the google spreadsheet with the data: https://docs.google.com/spreadsheets/d/1xgoOPu28dQSSGPIp_HHQs0uvvcyLNdkMF9XtRajhhxU/edit#gid=1193315437

## Contributors
Contributors to the code are:
Petra Isenberg, Natkamon Tovanich, and Tobias Isenberg

## How to update
You should first open the jupyter notebook found in the folder: vispubdata-update. A few things you can already do:
- get an IEEEXplore API key: https://developer.ieee.org/
- download the latest data from DBLP: https://dblp.org/xml/
- ask the IEEE VIS publications chairs for the titles of the year of IEEE VIS you'd like to add


Then open the jupyter notebooks in the respective folders in this order:
1. dblp-data-extraction
2. vispubdata-update
3. aminer-citation-update

If you have any problems then contact petra.isenberg@inria.fr
