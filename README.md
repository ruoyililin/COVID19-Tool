# COVID19-Tool
This repository contains a tool for presenting global Covid-19 cases and mortality statistics. The tool employs Beautiful Soup for web scraping, and uses pandas, numpy, and matplotlib for efficient data manipulation and visualization. This is a final project for a Python course at the École Normal Superior (Paris). 

## Summary
This project focuses on gathering, analyzing, and visualizing global Covid-19 data through web scraping, data manipulation, and graphical representation.

## Instructions
1. Download the whole folder. 
2. Install the necessaries packages and run `coronavirus_graphs.py`.
3. Interact with the interface to produce the desired graphs.

## Description of the code 
### Part I: Gather the Data 
`crawler.py` reads and webscraps data. 
- Input: `worldcities.csv`
- Output: `coronavirus_data.csv`

Contains the following functions: 

1. **cases_deaths:** Crawl data from [this link](https://bit.ly/3din7Bs), returning a 2D numpy array with country, cases, deaths, and region. Remove commas from numbers, replace "Japan (+Diamond Princess)" with "Japan", and remove "MS Zaandam".
2. **population:** Crawl data from [this link](https://bit.ly/3lWkVDO), returning a 2D numpy array with country and population size.
3. **capital_coordinates:** Read `worldcities.csv` to create a 2D numpy array with country and capital coordinates.
4. **main:** Create `coronavirus_data.csv` with combined data. 

### Part II: Analyze the Data 
`coronavirus_statistics.py` reads `coronavirus_data.csv` and analyses the data. 
- Input: `coronavirus_statistics.csv`
- Ouput: N/A

Contains the following functions: 

1. **read_data:** Read `coronavirus_data.csv` into a numpy array.
2. **region_data:** Return a 2D numpy array with region, cases, deaths, and population.
3. **country_data:** Return a 2D numpy array for specified countries, normalized by population.
4. **top_country_data:** Return a 2D numpy array of top `k` countries with the highest death rates, for countries with population size at least `n`.

### Part III: Visualize the Data 
`coronavirus_graphs.py` provides visualisation of the data. 

Contains the following functions: 
1. **regions_piechart:** Draw a pie chart for a region, showing deaths and recoveries.
2. **countries_barchart:** Draw bar charts for specified countries showing cases and deaths per million.
3. **highest_mortality:** Draw a bar chart for top `k` countries with the highest deaths per million, for countries with population size at least `n`.
4. **map:** Draw a map with circles representing the highest mortality rates. Use Cartopy.
5. **main:** Interact with the user to draw graphs based on their input.
