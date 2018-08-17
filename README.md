This navigates the website of the Australian parliament and downloads the daily Hansard transcripts in xml format.

It is currently hard-coded to download transcripts starting from 01-01-2018.

## Dependencies

* python3
* scrapy

## How to run

Clone or download the repository, then run 

```
scrapy crawl hansard
```

at the terminal from the top-level directory. The transcripts will be placed in a single file called 'hansard.xml'.
