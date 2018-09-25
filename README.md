This navigates the website of the Australian parliament and downloads the daily Hansard transcripts in xml format.

It is currently hard-coded to download transcripts starting after the 2013 election.

## Dependencies

* python3
    * BeautifulSoup
    * pandas
    * scrapy
* jupyter

## How to run

Clone or download the repository, then run 

```
scrapy crawl hansard
```

at the terminal from the top-level directory. The transcripts will be placed in the data directory. To process the XML files to produce the CSVs, run 

```
jupyter nbconvert --execute --ExecutePreprocessor.timeout=-1  process_speeches.ipynb 
```

The CSV files will be placed in ../tidied_parliamentary_data

A less horrendously inefficient scraper might start from [this](http://parlinfo.aph.gov.au/parlInfo/search/summary/summary.w3p;adv=yes;orderBy=customrank;page=0;query=Dataset%3Ahansards,hansards80%20Title%3A%22Start%20of%20Business%22;resCount=Default) search results page.
