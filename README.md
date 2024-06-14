# Vispubdata Reproducibility and Update

The code in this repository relates to the [VisPubData](http://www.vispubdata.org/) collection of publications in the field of visualization. For more information please check the [corresponding publication about the project](https://doi.org/10.1109/TVCG.2016.2615308):

Petra Isenberg, Florian Heimerl, Steffen Koch, Tobias Isenberg, Panpan Xu, Charles D. Stolper, Michael Sedlmair, Jian Chen, Torsten Möller, and John Stasko. vispubdata.org: A Metadata Collection about IEEE Visualization (VIS) Publications. IEEE Transactions on Visualization and Computer Graphics, 23(9):2199–2206, September 2017. doi: [10.1109/TVCG.2016.2615308](https://doi.org/10.1109/TVCG.2016.2615308)

If you use this data, we would appreciate a publication to this paper:
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
Petra Isenberg, Natkamon Tovanich, and Tobias Isenberg

## Code Purposes

There are two types of code in this reposotory, one for reproduing one of the figures we show in the paper mentioned above (for the purpose of showing reproducibility via the [Graphics Replicability Stamp Initiative](https://www.replicabilitystamp.org/)), and the other code for supporting the continued update of the dataset.

## Paper reproducibility

work in progress ...

## How to update
This code will allow to create an update of the vispubdata dataset you can find here: https://sites.google.com/site/vispubdata. If you have only small fixes of the data to report you might be better off to leave a comment on the google spreadsheet with the data: https://docs.google.com/spreadsheets/d/1xgoOPu28dQSSGPIp_HHQs0uvvcyLNdkMF9XtRajhhxU/edit#gid=1193315437

You should first open the Jupyter notebook found in the folder [`vispubdata-update/`](vispubdata-update/). A few things you can already do:
- get an IEEEXplore API key: https://developer.ieee.org/
- download the latest data from DBLP: https://dblp.org/xml/
- ask the IEEE VIS publications chairs for the titles of the year of IEEE VIS you'd like to add
- find the DOIs of the papers awarded in the year of the conference you'd like to add (you can try https://ieeevis.org)
- find the graphics replicability stamp papers (Tobias Isenberg can help you) of the year you'd like to add

Then open the Jupyter notebooks in the respective folders in this order:
1. [`dblp-data-extraction/`](dblp-data-extraction/)
2. [`vispubdata-update/`](vispubdata-update/)
3. [`aminer-citation-update/`](aminer-citation-update/)

If you have any problems then please contact petra.isenberg@inria.fr
