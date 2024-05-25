
#############################################################################################

# Part II: Analysing the data

#############################################################################################

# Author: Ruoyi Li 
# Date: 25/06/2023



# LOAD PACKAGES
import numpy as np


# DEFINE FUNCTIONS 
def read_data():
    """
    Reads the data from the coronavirus_data.csv file and returns it as a NumPy array.
    """
    data = []
    with open('coronavirus_data.csv', 'r') as file:
        lines = file.readlines()

        # Iterate over the lines (excluding the header)
        for line in lines[1:]:
            # Split the line by comma split(',') and strip whitespace, newlines strip()
            # a list comprehension that iterates over each value in the list
            row = [value.strip() for value in line.split(',')]
            data.append(row)

    # Convert the data list into a NumPy array
    data_array = np.array(data)
    return data_array 


def region_data():
    """
    This function takes a 2D numpy array containing country-level data and returns a 2D numpy array
    where each line contains: a region, number of cases, number of deaths, and population for that region.
    """

    # Load data. 
    # Variables are ['country', 'cases', 'deaths', 'region', 'population', 'latitude', 'longitude']
    data = read_data()

    # Replace "Australia/Oceania" with "Australia-Oceania" in the region column
    data[:, 3][data[:, 3] == 'Australia/Oceania'] = 'Australia-Oceania'
    
    # Get unique regions from the data
    regions = np.unique(data[:, 3])

    # Initialize empty lists to store region data
    region_cases = []
    region_deaths = []
    region_population = []

    # Iterate over each region
    for region in regions:
        # Filter data for the current region
        region_data = data[data[:, 3] == region]

        # Get the sum of cases, deaths, and population for the region
        total_cases = np.sum(region_data[:, 1].astype(int))
        total_deaths = np.sum(region_data[:, 2].astype(int))
        total_population = np.sum(region_data[:, 4].astype(int))

        # Append the region data to the respective lists
        region_cases.append(total_cases)
        region_deaths.append(total_deaths)
        region_population.append(total_population)

    # Stack the region data horizontally to create the region data array
    # The column_stack() function expects multiple arrays as separate arguments. 
    # By using a tuple, we can conveniently group the arrays together without the need for additional syntax,
    # such as enclosing the arrays in a list or using multiple parentheses
    region_data_array = np.column_stack((regions, region_cases, region_deaths, region_population))

    return region_data_array



def country_data(countries = None):
    """
    This function receives a list of countries (optional) and returns a 2D numpy array
    where each line contains: country, number of cases normalized by population,
    number of deaths normalized by population, and population.
    If no countries are provided, it considers all countries in the data.
    """
    # Load data
    #  # Variables are ['country', 'cases', 'deaths', 'region', 'population', 'latitude', 'longitude']
    data = read_data()

    # Filter data based on the list of countries (if provided)
    if countries is not None:
        data = data[np.isin(data[:, 0], countries)]

    # Extract relevant columns from the data
    country_names = data[:, 0]
    cases = data[:, 1].astype(int)
    deaths = data[:, 2].astype(int)
    population = data[:, 4].astype(int)

    # Calculate normalized values
    cases_normalized = cases / population
    deaths_normalized = deaths / population

    # Create the country data array
    country_data_array = np.column_stack((country_names, cases_normalized, deaths_normalized, population))

    return country_data_array



def top_country_data(k, n = 0):
    """
    This function receives two integers k and n and returns a 2D numpy array.
    The array contains k lines of the format country, number of deaths normalized
    by the size of the population, latitude, longitude. 
    The countries included in the array are the subset of countries with population size 
    at least n that have the highest number of deaths normalized by the size of the population. 
    The argument n is optional with n = 0 by default.
    """
    # Load data
    # Variables order is ['country', 'cases', 'deaths', 'region', 'population', 'latitude', 'longitude'] 
    data = read_data()

    # Filter the country data based on population size
    
    data = data[data[:, 4].astype(int) >= n]

    # Normalized deaths by population
    data[:,2] = data[:,2].astype(float)/data[:,4].astype(float) 

    # Sort the filtered data based on deaths normalized by population: ascending order
    # Indexing the data array with the sorted indices 
    sorted_data = data[np.argsort(data[:,2].astype(float))]

    # Select the top k countries with highest deaths normalized by population
    # Negative indexing allows you to count from the end of the array. 
    top_countries = sorted_data[-k:] 

    # Select the all the rows of the relevant columns 
    result = top_countries[:,[0,2,5,6]]
    
    return result



