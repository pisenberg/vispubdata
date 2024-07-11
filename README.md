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
[Petra Isenberg](https://petra.isenberg.cc/), [Natkamon Tovanich](https://www.linkedin.com/in/natkamon-tovanich-00a1a5aa/), and [Tobias Isenberg](https://tobias.isenberg.cc/)

## Code Purposes

There are two types of code in this repository, one for reproduing one of the figures we show in the paper mentioned above (for the purpose of showing reproducibility via the [Graphics Replicability Stamp Initiative](https://www.replicabilitystamp.org/)), and the other code for supporting the continued update of the dataset.

## Paper reproducibility

The code in the [`reproducibility/`](reproducibility/) subdirectory facilitates the reproduction of the plot in Figure 1 of the [corresponding paper](https://doi.org/10.1109/TVCG.2016.2615308), albeit adjusted to the updated data in the dataset (as of writing this text, years 2016–2023 of the IEEE VIS conference have been added). The other figures in the paper are a manually created overview of the conference evolution (Figure 2; for that see the files in the [`naming-graphic/`](naming-graphic/) subdirectory of this repository) and screenshots of the dataset in use by other tools (Figures 3–5). The original version of Figure 1 from the paper looks as follows:

![Figure 1 of VisPubData publication](reproducibility/figure1-original.png "Figure 1 of VisPubData publication (image is in the public domain)")
(image is in the public domain)

### Prerequisites
* a Python 3 installation; e.g., https://www.python.org/downloads/ or https://www.anaconda.com/download/
* dedicated Python libraries installed with `pip3` or `conda` as follows (or similar):
    * `altair`: `pip3 install altair` or `conda install -c conda-forge altair` (see https://altair-viz.github.io/)
    * `vl-convert`: `pip3 install vl-convert-python` or `conda install -c conda-forge vl-convert-python` (see https://altair-viz.github.io/user_guide/saving_charts.html)
    * `pandas`: `pip3 install pandas` (see https://pandas.pydata.org/docs/getting_started/install.html; already included in Anaconda)
    * the file [`reproducibility/requirements.txt`](reproducibility/requirements.txt) includes all of these requirements, install them all in one go with `pip3 install -r reproducibility/requirements.txt`

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
(the image is available under the [Creative Commons Attribution 4.0 International (CC BY 4.0) license](https://creativecommons.org/licenses/by/4.0/); please attribute the image to the [contributors named above](#contributors) and cite [the mentioned journal paper](https://doi.org/10.1109/TVCG.2016.2615308))

Notice that the labels have been reworded slightly to reflect the changes that happened in the conference in the meantime as well as to make the distinction between journal conference papers and pure journal papers presented at the conference more clear, and that the labels are ordered differently from the original figure due to the use of a new plotting tool.

## How to update the VisPubData dataset
This code will allow you to create an update of the [VisPubData dataset](http://www.vispubdata.org/). If you have only small fixes of the data to report you might be better off to leave a comment on the [Google spreadsheet with the data](https://docs.google.com/spreadsheets/d/1xgoOPu28dQSSGPIp_HHQs0uvvcyLNdkMF9XtRajhhxU/edit#gid=1193315437) and to e-mail petra.isenberg@inria.fr to make the change for you. If, however, you would like to, for example, add a new year to the dataset or create a local update for yourself, then read on.

### Prerequisits
- A Python 3 installation, we recommend [Anaconda](https://www.anaconda.com/download/).
- Several additional Python packages:
  - [lxml](https://lxml.de/)
  - [requests](https://pypi.org/project/requests/)
  - [crossrefapi](https://github.com/fabiobatalha/crossrefapi)
  - [tqdm](https://tqdm.github.io/)
  - The file [`requirements.txt`](requirements.txt) includes all of these requirements, install them all in one go with `pip3 install -r requirements.txt`.
- Get an IEEEXplore API key: https://developer.ieee.org/ (this may take a few days). Then make a copy of [`vispubdata-update/ieeexplore-apikey-template.txt`](vispubdata-update/ieeexplore-apikey-template.txt) and call it [`vispubdata-update/ieeexplore-apikey.txt`](vispubdata-update/ieeexplore-apikey.txt), and replace the `xxxxxxxxxxxxxxxxxxxxxxxx` in the renamed copy you made with your API key.
- Download the latest data from the [DBLP]( https://dblp.org/): go to https://dblp.org/xml/ and download the files `dblp.xml.gz` and `dblp.dtd` and put them into the [`dblp-data-extraction/data/`](dblp-data-extraction/data/) subfolder in this repository. Also do not forget to extract the `dblp.xml.gz` to `dblp.xml`.
- You need to get a list of papers actually accepted to and presented at IEEE VIS (i.e., those papers initially submitted at the end-of-March deadline and then accepted to IEEE VIS). Ask the [IEEE VIS](https://ieeevis.org/) [program chairs](mailto:program@ieeevis.org) for the titles of the year of IEEE VIS you'd like to add. Also find the DOIs of the papers awarded in the year of the conference you would like to add (you can try https://ieeevis.org, or check on https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=2945, or on https://www.computer.org/csdl/journal/tg; the IEEE VIS proceedings are **typically** the first issue in a TVCG volume/year). You will need this data in the process to cross-check and verify which papers to include from the downloaded data from IEEE Xplore.
- Get a list of papers with a [graphics replicability stamp](), not only for the year you want to add but for all years because the stamps are awarded retroactively. This list should contain the DOIs of the papers with a GRSI stamp (in no particular order), and it can include more papers than in the VisPubData database (because the GRSI is not limited to visualization papers). The script `extract-tvcg-dois-with-stamp.py` in [Tobias Isenberg](https://tobias.isenberg.cc/)'s [Visualization-Reproducibility repository](https://github.com/tobiasisenberg/Visualization-Reproducibility) generates such a list, if you need help just contact [Tobias](https://tobias.isenberg.cc/). Place the resulting CSV file into the [`vispubdata-update/`](vispubdata-update/) subdirectory, overwriting the existing [`vispubdata-update/tvcg-dois-with-stamp.csv`](vispubdata-update/tvcg-dois-with-stamp.csv) file. This step is not essential to be able to run things, as the repository already contains a [`vispubdata-update/tvcg-dois-with-stamp.csv`](vispubdata-update/tvcg-dois-with-stamp.csv) file with data on the GRSI up to a point. But it would, of course, be better to have up-to-date data.

### Start the Jupyter notebook server
- Navigate to the main folder of this repsitory (the top folder) using the [command line](https://docs.jupyter.org/en/latest/glossary.html#term-command-line). If you are on [Anaconda Python](https://www.anaconda.com/) it is best to do this using the Anaconda prompt.
- Start the Jupyter notebook server there by calling:
  ```
  jupyter notebook
  ```
  This will open a browser window and show the subfolders of the repository and the included files.
- If this does not work out of the box, you can get more help here: https://docs.jupyter.org/en/latest/install.html

### Ready? Let's go...
Then use the newly opened browser window to open the the Jupyter notebooks in the respective folders in the order they are named below (double-click on the folder, then double-click on the respective `ipynb` file, which opens it in a new browser tab). Each Jupyter notebook contains additional prerequisites and the instructions for running it.
1. [`dblp-data-extraction/ParseDBLP-VIS-Authors.ipynb`](dblp-data-extraction/ParseDBLP-VIS-Authors.ipynb)
    - The last step in this notebook will take several minutes, depending on your machine and the size of the data. The script, however, shows its progress in iterations (in batches of 100,000) and iterations per second.
    - Unfortunately it is not possible to compute a percentage as the total number of needed iterations is not known ahead of time. The total number of needed iterations depends on the size of the DBLP data when downloaded and should be in the order of 97,000,000 (at time of writing these instructions) or more.
    - So just wait as long as these iteration counts continue to be updated.
    - If error messages appear check that you have the downloaded DBLP data files (according to the instructions above) and placed them into the [`dblp-data-extraction/data/`](dblp-data-extraction/data/) subfolder and that you also uncompressed the `dblp.xml.gz` file.
    - The script is done when you see a note that reports how many articles were found and the script prints `DONE`.
    - You can the close the window with the Jypiter notebook, as the results have been saved as an updated version of [`dblp-data-extraction/data/VIS-author-articles.csv`](dblp-data-extraction/data/VIS-author-articles.csv).
2. [`vispubdata-update/Vispubdata update IEEE VIS papers.ipynb`](vispubdata-update/Vispubdata%20update%20IEEE%20VIS%20papers.ipynb)
    - This process is quite involved, carefully read and follow the instructions in the notebook.
    - Again, some of its processing may take a while (e.g., the CrossRef data check in the order of an hour or more), but there are one again progress indicators.
    - Once done, many of the data files in the subdirectory are updated and you can close the browser tab.
3. [`vispubdata-update/journals-at-vis-update.ipynb`](vispubdata-update/journals-at-vis-update.ipynb)
    - Again, some of its processing may take a while (e.g., the CrossRef data check in the order of 10 minutes or more), but there are one again progress indicators.
    - Once done, many of the data files in the subdirectory are updated and you can close the browser tab.
4. [`aminer-citation-update/first_scan.ipynb`](aminer-citation-update/first_scan.ipynb)
5. [`aminer-citation-update/merge_data.ipynb`](aminer-citation-update/merge_data.ipynb)

The final results of the process can then be found in the files [`vispubdata-update/results/vispubdata-update.csv`](vispubdata-update/results/vispubdata-update.csv) and [`vispubdata-update/results/vispubdata-update-journals.csv`](vispubdata-update/results/vispubdata-update-journals.csv) as well as the Aminer citations at  [`vispubdata-update/results/vispubdata-update.csv-aminer.csv`](vispubdata-update/results/vispubdata-update.csv-aminer.csv) and [`vispubdata-update/results/vispubdata-update-journals.csv-aminer.csv`](vispubdata-update/results/vispubdata-update-journals.csv-aminer.csv), which could technically be used to update the VisPubData Google spreadsheet (for those with access to it).

If you have any problems then please contact petra.isenberg@inria.fr.
