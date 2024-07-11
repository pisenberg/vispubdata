# VisPubData Reproducibility and Update

The code in this repository relates to the [VisPubData](http://www.vispubdata.org/) collection of publications in the field of visualization. For more information please check the [corresponding publication about the project](https://doi.org/10.1109/TVCG.2016.2615308):

Petra Isenberg, Florian Heimerl, Steffen Koch, Tobias Isenberg, Panpan Xu, Charles D. Stolper, Michael Sedlmair, Jian Chen, Torsten Möller, and John Stasko. vispubdata.org: A Metadata Collection about IEEE Visualization (VIS) Publications. IEEE Transactions on Visualization and Computer Graphics, 23(9):2199–2206, September 2017. doi: [10.1109/TVCG.2016.2615308](https://doi.org/10.1109/TVCG.2016.2615308)

If you use this data, we would appreciate a citation to our paper:
```
@article{Isenberg:2017:VMC,
  author      = {Petra Isenberg and Florian Heimerl and Steffen Koch and Tobias Isenberg and Panpan Xu and Charles D. Stolper and Michael Sedlmair and Jian Chen and Torsten M{\"o}ller and John Stasko},
  title       = {vispubdata.org: A Metadata Collection about {IEEE} Visualization ({VIS}) Publications},
  journal     = {IEEE Transactions on Visualization and Computer Graphics},
  year        = {2017},
  volume      = {23},
  number      = {9},
  month       = sep,
  pages       = {2199--2206},
  doi         = {10.1109/TVCG.2016.2615308},
  oa_hal_url  = {https://hal.science/hal-01376597},
  url         = {http://www.vispubdata.org/site/vispubdata/},
}
```

## Contributors
Contributors to the code are:
[Petra Isenberg](), Natkamon Tovanich, and [Tobias Isenberg]()

## Code Purposes

There are two types of code in this repository, one for reproduing one of the figures we show in the paper mentioned above (for the purpose of showing reproducibility via the [Graphics Replicability Stamp Initiative](https://www.replicabilitystamp.org/)), and the other code for supporting the continued update of the dataset.

## Paper reproducibility

The code in the [`reproducibility/`](reproducibility/) subdirectory facilitates the reproduction of the plot in Figure 1 of the [corresponding paper](https://doi.org/10.1109/TVCG.2016.2615308), albeit adjusted to the updated data in the dataset (as of writing this text, years 2016–2023 of the IEEE VIS conference have been added). The other figures in the paper are a manually created overview of the conference evolution (Figure 2) and screenshots of the dataset in use by other tools (Figures 3–5). The original version of Figure 1 from the paper looks as follows:

![Figure 1 of VisPubData publication](reproducibility/figure1-original.png "Figure 1 of VisPubData publication (image is in the public domain)")
(image is in the public domain)

### Prerequisites
* a Python 3 installation; e.g., https://www.python.org/downloads/ or https://www.anaconda.com/download/
* dedicated Python libraries installed with `pip3` or `conda` as follows (or similar):
    * `altair`: `pip3 install altair` or `conda install -c conda-forge altair` (see https://altair-viz.github.io/)
    * `vl-convert`: `pip3 install vl-convert-python` or `conda install -c conda-forge vl-convert-python` (see https://altair-viz.github.io/user_guide/saving_charts.html)
    * a [`reproducibility/requirements.txt`](reproducibility/requirements.txt) includes all of these requirements, install them with `pip3 install -r reproducibility/requirements.txt`
    * `pandas`: `pip3 install pandas` (see https://pandas.pydata.org/docs/getting_started/install.html; already included in Anaconda)

### Running the script

The [`reproducibility/reproducibility.py`](reproducibility/reproducibility.py) script essentially loads the current state of the dataset  and then directly produces the new version of the figure in the local directory. There are two ways to get the data. By default, the data is pulled directly from the respective Google Spreadsheets, and the script should run without any further configuration.

Alternatively, one can also download the data to local `csv` files and then run everything locally. For that, please set
```
useFiles = True
```
in the configuration section of the [`reproducibility/reproducibility.py`](reproducibility/reproducibility.py) script at the top, and then download the data as follows: Please first go to the shared [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1xgoOPu28dQSSGPIp_HHQs0uvvcyLNdkMF9XtRajhhxU/edit?usp=sharing) that contains the VisPubData dataset, make sure that the first tab on the bottom is selected ("Main dataset"), and then download the data using the menu via File > Download > Comma Separated Values (.csv) and then save the file to `reproducibility/vispubdata.csv`. Next, please go to the shared [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1I6n4a6xvmoanAIDiSsGlaOVljAJ5IkT2C_naI-dStNo/edit?usp=sharing) that contains the data about the journal presentations, and then download that dataset the same way as before and save the file to `reproducibility/vis-journal-presentations.csv`. Then everything is in place to run the script.

To run the script in either case, simply do:
```
cd reproducibility/
python3 reproducibility.py
```

The script then produces the equivalent of Figure 1 of the paper as `reproducibility/reproducibility.pdf`, but updated to the most recent version of the dataset, which looks like this (2023 version):

![udated version of Figure 1 of VisPubData publication](reproducibility/figure1-updated.png "updated version of Figure 1 of VisPubData publication (image is available under the CC BY 4.0 license)")
(the image is available under the [Creative Commons Attribution 4.0 International (CC BY 4.0) license](https://creativecommons.org/licenses/by/4.0/))

Notice that the labels have been reworded slightly to reflect the changes that happened in the conference in the meantime as well as to make the distinction between journal conference papers and pure journal papers presented at the conference more clear, and that the labels are ordered differently from the original figure due to the use of a new plotting tool.

## How to update the VisPubData dataset
This code will allow to create an update of the [VisPubData dataset](http://www.vispubdata.org/). If you have only small fixes of the data to report you might be better off to leave a comment on the [Google spreadsheet with the data](https://docs.google.com/spreadsheets/d/1xgoOPu28dQSSGPIp_HHQs0uvvcyLNdkMF9XtRajhhxU/edit#gid=1193315437) and email petra.isenberg@inria.fr to make the change for you. If, however, you would like to, for example, add a new year to the dataset, then read on.

First open the Jupyter notebook server in the main folder of this repositiry. 

### How to start a jupyter notebook?
- navigate to the main folder of this repsitory using the [command line|https://docs.jupyter.org/en/latest/glossary.html#term-command-line]. If you are on Anaconda python it's best to do this using the Anaconda prompt.
- start the jupyter notebook there using by calling ''jupyter notebook''.
- If this doesn't work out of the box, get more help here: https://docs.jupyter.org/en/latest/install.html

### What else do I need?
 However, in preparation, there are a few things you can already do.

- get an IEEEXplore API key: https://developer.ieee.org/
- download the latest data from DBLP: https://dblp.org/xml/
- ask the IEEE VIS publications chairs for the titles of the year of IEEE VIS you'd like to add
- find the DOIs of the papers awarded in the year of the conference you'd like to add (you can try https://ieeevis.org)
- find the graphics replicability stamp papers (Tobias Isenberg can help you) of the year you'd like to add

### Which python modules do I need?
There are a lot of them, many come with python. But you also need:
- [lxml](https://lxml.de/)
- [requests](https://pypi.org/project/requests/)
- [crossrefapi](https://github.com/fabiobatalha/crossrefapi)

### Ready? Let's go...
Then open the Jupyter notebooks in the respective folders in this order. Each jupyter notebook contains the instructions for running it.
1. [`dblp-data-extraction/`](dblp-data-extraction/): 'ParseDBLP-VIS-Authors.ipynb'
2. [`vispubdata-update/`](vispubdata-update/): 'Vispubdata update IEEE VIS papers.ipynb'
3. [`aminer-citation-update/`](aminer-citation-update/)

If you have any problems then please contact petra.isenberg@inria.fr
