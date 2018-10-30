# Indian Polling Stations

This code scrapes Indian electoral polling stations from [Polling Station Locations, Electoral Commission of India](http://psleci.nic.in/).  

## Data

Data gathered on April 14th - 15th, 2017. There are *905,421* observations.

Data is contained in [out.zip](out.zip) (18MB). Inside this ZIP file is an uncompressed CSV file, out.csv (135MB). Note that text strings have been downconverted from Unicode to ASCII where appropriate (using Python `unidecode`); if you are using data to match with existing Indian datasets, you may need to downconvert their text labels as well.

Example data:

| State | District | AC | Latitude | Longitude | PS Number | PS Name | URL |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Telangana | Khammam | Aswaraopeta  | 17.381287 | 80.709979 | 30 | ABBUGUDEM | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=30) |
| Telangana | Khammam | Aswaraopeta  | 17.276105 | 81.046777 | 131 | ACHUTHAPURAM | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=131) |
| Telangana | Khammam | Aswaraopeta  | 17.19378325 | 80.99154315 | 85 | ALLIPALLI | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=85) |
| Telangana | Khammam | Aswaraopeta  | 17.361801 | 81.195683 | 157 | ANANTHARAM | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=157) |
| Telangana | Khammam | Aswaraopeta  | 17.373627 | 80.963417 | 114 | ANKAMPALEM | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=114) |
| Telangana | Khammam | Aswaraopeta  | 17.36768 | 80.775935 | 67 | ANNAPUREDDYPALLI | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=67) |
| Telangana | Khammam | Aswaraopeta  | 17.36768 | 80.775935 | 68 | ANNAPUREDDYPALLI | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=68) |
| Telangana | Khammam | Aswaraopeta  | 17.36768 | 80.775935 | 69 | ANNAPUREDDYPALLI | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=69) |
| Telangana | Khammam | Aswaraopeta  | 17.391797 | 80.961505 | 115 | ARLAPENTA H/o ANKAMPALEM | [Click](http://psleci.nic.in/pslinfoc.aspx?S=S29&A=118&P=115) |

## Instructions to re-scrape data

0. Install required Python pre-requisites (`pip install -r requirements.txt`)
1. Run `psleci.py` to scrape State, District, AC triples from the website to prepare the main scraper and store in `triples.json`
2. Run `polling_stations.py` to scrape the information
3. Data is now contained in `out.csv`. Errors, if any, are output to `error.txt`

## Code Style Guide

`pylint` settings are contained in `.pylintrc`. 

`pep8` settings are as follows:
`pep8 --ignore W191,E101,E111,E501,E128`

## Contributions?

Please feel free to open a pull request.

![Map](map_make/map.png?raw=true "Sample polling stations")
