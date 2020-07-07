# Sigef Crawler

<small>_Optimized for python 3.6+_</small>

This project aims in crawling through sigef pages, extract information and 
parses it into a csv file.

----------------------

## Dependencies

For installing the requirements, in your ___venv___ or ___anaconda env___, 
just run the following command:

```shell script
pip install -r requirements.txt
```
----------------

## Project's Structure

```bash 
.
└── sigef-crawler
    ├── data
    │   ├── links.txt
    │   └── outputs
    │       ├── sigef-2020-07-05.csv
    │       ├── sigef-2020-07-06.csv
    │       └── sigef-2020-07-07.csv
    ├── docs
    │   └── CREDITS
    ├── src
    │   ├── __init__.py
    │   └── crawler.py
    ├── tests
    │   └── unittests
    │       └── __init__.py
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requirements.txt
```

#### Directory description

- __data:__ The data dir. Group of non-script support files.
- __docs:__ The documentation dir.
- __src:__ The scripts & source code dir.
- __tests:__ The unittests dir.

----------------

## Usage Notes

Section aimed on clarifying some running issues.

### Running

For running it, at the `~/src` directory just run:

```shell script
python crawler.py
``` 

or, if importing it as a module, just run:
````python
from crawler import SigefRequests

if __name__ == '__main__':
    SigefRequests('path/to/file').__call__()
````

---------------
