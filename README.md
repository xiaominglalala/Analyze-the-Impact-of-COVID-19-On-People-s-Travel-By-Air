# Introduction

This repo is the final project of group `Segmentation Fault`.

Group member: 

- Rui CHen
- Yutai Li
- Yuming Wang
- Boning Zhang

here is the structure of this repo. We skip a few files to make it clear to look.

```shell
├── content.html
├── content.md				# original content of websites
├── DA presentation.pptx	# presentation slides
├── network_code/			# network analysis codes
│   ├── Data_opensky/
│   ├── opensky/
│   ├── opensky_network_analysis.py
│   ├── opensky_network_Visualize.py
│   ├── opensky_preprocess.py
│   ├── __pycache__/
│   └── readMe.md
├── README.md				# this file
└── web/					# website directory
    ├── analysis/			# analysis sub page
    ├── analysis.html
    ├── conclusion.html
    ├── css/				# css directory
    ├── data.html
    ├── figures/			# figures related to the whole project
    ├── fonts/				# fonts
    ├── future.html
    ├── images/				# website related images
    ├── index.html
    ├── js/					# website related javascripts
    ├── preprocess.html
    ├── sample_cdc.html
    ├── sample_opensky.html	
    ├── sample_twitter.html	
    └── templates/			# templates of websites

12 directories, 131 files
```



# Web

Everything related to website is in directory `web`. We already deployed it on our server. Click [cosc587.coreja.com](http://cosc587.coreja.com) to check it.

If you wanna see it yourself other than the one that we deployed, make sure to deployed it on a web server like `nginx` or `apache http server` to get the best experience.

The contents of our website are mostly written in `content.md`, `content.html` is the export version of its markdown file.

For our generated `plotly` figures, they are already embedded in our website. They are in the directory `figures`.
