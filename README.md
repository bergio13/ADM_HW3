# Homework 3 - ADM
**Consider only the `main` branch.**

This repository contains the Homework 3 for the ADM course. In particular:
- the notebook `HW3.ipynb` is the notebook containing the answers to the questions of the homework
- the folder `modules` contains the python files with some of the function we created and used in the notebook
  - `prepro.py` contains the functions used to preprocess the text
  - `crawler.py` the functions used to crawl the website
  - `myparser.py` the functions used to parse the info fro the html pages
- the folder `outputs` contains some files created during the homework, specifically:
  - `vocabulary.pkl` and `inverted_indx.pkl` are the dictionaries created as output of two functions of Q2
  - `master_urls.txt` is the list of urls created in Q1
  - `course_info.tsv` is the file containing the info parsed from the HTML pages for the 6000 master degrees
  - `merged_file.tsv` is merged tsv file of all course_i.tsv files created in point 1.
  - `msc_file.tsv`is a merged file of all the MSc courses.
  - `country_count.txt` is the name of the country that offers the most Master's Degrees.
  - `city_count.txt` is the name of the city in that country that offers the most Master's Degrees.
  - `engcourses.tsv` is the tsv file of all the engineering courses.
- the file `CommandLine.sh` contains the executable script for the Command Line Question.

(If you are interested in looking also at the downloaded html pages and the tsv files you can find them in the `master` branch, in the `master_pages` and `course_info` folders repectively)
  
