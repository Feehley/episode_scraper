# TLDR;
Scrape Episodes from ISO disk files \
Only tested on Ubuntu 22.04

## Usage
$ ls \
testfile.iso \
\
$ python3&emsp;episode_scraper.py&emsp;testfile.iso \
 100%|█████████████████████████████████████████████████████████████████| 6/6 [08:11, 98.31s/it] 

$ ls \
episode_scraper.py&emsp;Episodes&emsp;testfile.iso 


$ python3 episode_scraper testfile.iso -l24 -d -o TEST \
 100%|█████████████████████████████████████████████████████████████████| 6/6 [08:11, 98.31s/it] \
 [[1, 110000], [2, 88766], [3, 303367], [4, 260967], [5, 284000], [6, 305934], [7, 98500], [8, 110000], [9, 104766], [10, 308834], [11, 263500], [12, 300033], [13, 265900], [14, 98500], [15, 110000], [16, 110766], [17, 277333], [18, 276000], [19, 301333], [20, 277600], [21, 98500], [22, 110000], [23, 88899], [24, 300867], [25, 258300], [26, 326500], [27, 268467], [28, 98500], [29, 110000], [30, 84866], [31, 284333], [32, 283834], [33, 319667], [34, 270333], [35, 98500], [36, 110000], [37, 130766], [38, 300166], [39, 222166], [40, 309333], [41, 280600], [42, 98500], [43, 110000], [44, 74766], [45, 284033], [46, 252300], [47, 291500], [48, 340433], [49, 97000], [50, 12500], [51, 500]]\
{1: [1, 2, 3, 4, 5, 6, 7], 2: [8, 9, 10, 11, 12, 13, 14], 3: [15, 16, 17, 18, 19, 20, 21], 4: [22, 23, 24, 25, 26, 27, 28], 5: [29, 30, 31, 32, 33, 34, 35], 6: [36, 37, 38, 39, 40, 41, 42], 7: [43, 44, 45, 46, 47, 48, 49]}\
 100%|█████████████████████████████████████████████████████████████████| 6/6 [08:11, 98.31s/it] \
 \
$ ls \
episode_scraper.py&emsp;TEST&emsp;testfile.iso 

## Help
$ python3 episode_scraper.py -h \
usage: episode_scraper.py [-h] [-l EPISODE_LENGTH] [-c CHAPTERS] [-o OUTPUT] [-d] input\
\
positional arguments:\
&emsp;input&emsp;&emsp;Input file to parse into chapters\
  \
options:\
&emsp;-h, --help&emsp;&emsp;how this help message and exit\
&emsp;-l EPISODE_LENGTH,&emsp;--episode_length EPISODE_LENGTH\
&emsp;&emsp;&emsp;&emsp;&emsp;Average Episode length\
&emsp;-c CHAPTERS, --chapters CHAPTERS\
&emsp;&emsp;&emsp;&emsp;&emsp;Chapters per episode\
&emsp;-o OUTPUT, --output OUTPUT\
&emsp;&emsp;&emsp;&emsp;&emsp;output directory location\
&emsp;-d, --debug&emsp;&emsp;Enable debugging to see chapters and episodes\
