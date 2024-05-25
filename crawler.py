#############################################################################################

# Part I: Gather the data 

#############################################################################################

# Author: Ruoyi Li 
# Date: 25/06/2023



# LOAD PACKAGES
import requests
from bs4 import BeautifulSoup
import numpy as np
import os



# DEFINE FUNCTIONS
def cases_deaths():
    """
    This function returns a 2D numpy array by crawling https://bit.ly/3din7Bs. 
    Each line of the array contain four fields: 
    (1) country, (2) number of cases, (3) number of deaths, (4) region. 
    The function: 
    - removes commas from numbers (1,659 should look like 1659), 
    - replaces Japan (+Diamond Princess) with Japan, 
    - removes the entry corresponding to MS Zaandam (which is a ship).
    """
    # Send a GET request to the URL
    response = requests.get('https://bit.ly/3din7Bs')
        
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing the data
    table = soup.find('table')
    
    # Create empty lists to store the data
    data = []
    
    # Iterate over the rows of the table (skipping the header row)
    for row in table.find_all('tr')[1:]:
        # Extract the columns from one row. 
        # Object columns is a list with 4 elements  
        columns = row.find_all('td')
        
        # Extract the country, number of cases, number of deaths, and region
        country = columns[0].text.strip()
        cases = columns[1].text.strip().replace(',', '')
        deaths = columns[2].text.strip().replace(',', '')
        region = columns[3].text.strip()
        
        # Replace "Japan (+Diamond Princess)" with "Japan"
        if country == 'Japan (+Diamond Princess)':
            country = 'Japan'
        
        # Append the data to the list
        data.append([country, cases, deaths, region])
    
    # Convert the data list into a NumPy array
    array = np.array(data)
    
    # Remove the entry corresponding to MS Zaandam
    # Array [:,0] refers to all the rows of column 0 corresponding to country 
    array = array[array[:, 0] != 'MS Zaandam']
    
    # Finally, return the array
    return array



def population():
    """
    This function creates a 2D numpy array by crawling https://bit.ly/3lWkVDO.
    Each line contains two fields: country, size of the population.
    """
    # Send a GET request to the URL
    response = requests.get('https://bit.ly/3lWkVDO')

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the data
    table = soup.find('table')

    # Create an empty list to store the data
    data = []

    # Iterate over the rows of the table (skipping the header row)
    for row in table.find_all('tr')[1:]:
        # Extract the columns from the row
        columns = row.find_all('td')

        # Extract the country and population
        # Column 0 is the row number
        country = columns[1].text.strip()
        population = columns[2].text.strip().replace(',', '')

        # Append the data to the list
        data.append([country, population])

    # Convert the data list into a NumPy array
    pop_array = np.array(data)

    # Finally, return the array
    return pop_array




def capital_coordinates():
    """
    Reads the file worldcities.csv and creates a 2D NumPy array that contains
    the coordinates of the capital city for each country. If a country has 
    multiple capitals, one capital is selected at random.
    """
    # Get the path of the script when running in terminal 
    # path = os.path.dirname(os.path.abspath(__file__))
    
    # Get the path of the working directory when running in IDE
    path = os.getcwd()

    # Construct the path to the worldcities.csv file.
    # One should save the csv file in the same folder as the working directory or script
    csv_path = os.path.join(path, 'worldcities.csv')

    # Read the CSV file
    with open(csv_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Lines is a list. Each element of lines is a row of the csv

        # Extract the header row
        # .strip() is a string method that removes leading and trailing whitespace characters. In this case newlines
        # .split(',') is another string method that splits the string into a list of substrings 
        header = lines[0].strip().split(',')

        # Find the column indices for the required fields
        country_index = header.index('country')
        capital_index = header.index('capital')
        lat_index = header.index('lat')
        lng_index = header.index('lng')

        # Create an empty dictionary to store the selected capital coordinates for each country
        capital_coords = {}

        # Iterate over each line in the CSV file (excluding the header)
        for line in lines[1:]:
            values = line.strip().split(',')
            # values is a list containing a row. each element is a column of a row

            # Check if the city is a capital
            if values[capital_index] == 'primary':
                # Extract the country, latitude, and longitude
                country = values[country_index]
                latitude = values[lat_index]
                longitude = values[lng_index]

                # Check if the country already has a selected capital
                if country not in capital_coords:
                    # Add the capital coordinates to the dictionary for the country
                    # Key is the country and the value is the tuple (country, latitude, longitude)
                    capital_coords[country] = (country, latitude, longitude)

    # Convert the dictionary values into a 2D NumPy array
    coords_array = np.array(list(capital_coords.values()))

    return coords_array




def main():
    """
    This function creates the file coronavirus_data.csv. 
    In this file, each line of which contains the following fields: 
    country, number of cases, number of deaths, region, population, latitude, longitude. 
    """
    # Get the data arrays
    cases_deaths_data = cases_deaths()
    population_data = population()
    capital_coords_data = capital_coordinates()

    # Create a dictionary for cases and deaths data
    cases_deaths_dict = {}
    for row in cases_deaths_data:
        country = row[0]
        cases = row[1]
        deaths = row[2]
        region = row[3]
        cases_deaths_dict[country] = [cases, deaths, region]
        # key is country and values is the list of [cases, deaths, region]

    # Create a dictionary for population data
    population_dict = {}
    for row in population_data:
        country = row[0]
        population_val = row[1]
        population_dict[country] = population_val
        # key is country and value is population_val

    # Create a dictionary for capital coordinates
    capital_coords_dict = {}
    for row in capital_coords_data:
        country = row[0]
        latitude = row[1]
        longitude = row[2]
        capital_coords_dict[country] = [latitude, longitude]
        # key is country and value is the list of [latitude, longitude]

    # Merge the data based on country name
    merged_data = []
    for country in capital_coords_dict:
        if country in cases_deaths_dict and country in population_dict:
            # 3 variables and 3 elements
            cases, deaths, region = cases_deaths_dict[country]
            # 1 variable and 1 value
            population_val = population_dict[country]
            # 2 variables and 2 elements
            latitude, longitude = capital_coords_dict[country]
            merged_data.append([country, cases, deaths, region, population_val, latitude, longitude])

    # Write the merged data to the CSV file
    # The with statement ensures that the file is properly closed after writing or in case of an error.
    with open('coronavirus_data.csv', 'w', encoding='utf-8') as file:
        file.write('country,cases,deaths,region,population,latitude,longitude\n')
        # merged data is a list of list
        for row in merged_data:
            line = ','.join(str(value) for value in row)
            # joins the elements of the current row into a single string, separated by commas. 
            # It converts each value to a string using the str() function to ensure compatibility. 
            file.write(line + '\n')

    print("Data merged and saved to coronavirus_data.csv")


# Call the main function when running the script
if __name__ == "__main__":
    main()


