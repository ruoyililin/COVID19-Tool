
#############################################################################################

# Part III : Visualizing the data

#############################################################################################

# Author: Ruoyi Li 
# Date: 25/06/2023



# LOAD PACKAGES
import matplotlib.pyplot as plt
import numpy as np
import os
import coronavirus_statistics as cs 
import cartopy.crs as ccrs




# DEFINE FUNCTIONS 

def regions_piechart(region, show = False):
    """
    This function receives a region as an argument and draws a pie chart where
    one fraction corresponds to coronavirus deaths and one fraction corresponds
    to the number of people who contracted the virus and recovered. The pie chart
    is saved in the ./graphs folder with a unique name.
    """
    # Load data by region. 
    # Variables are in the following order ["Region", "Cases", "Deaths", "Population"] 
    data = cs.region_data()

    # Choose the relevant region 
    region_data = data[data[:, 0] == region]
    # Region data is a row [[]]

    # Retrieve data for the given region
    deaths = region_data[0, 2].astype(int)
    recovered = region_data[0, 1].astype(int) - deaths

    # Create labels and corresponding data values for the pie chart
    labels = ['Deaths', 'Recovered']
    data_values = [deaths, recovered]

    # Set colors for the pie chart
    colors = ['red', 'green']

    # Create the pie chart
    plt.pie(data_values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Set the title of the pie chart
    plt.title(f'COVID-19 Statistics for {region}')

    # Get the path of the script: from terminal 
    # script_path = os.path.dirname(os.path.abspath(__file__))
    
    # Get the path of the working directory
    script_path = os.getcwd()

    # Create the graphs folder if it doesn't exist
    graphs_folder = os.path.join(script_path, 'graphs')
    if not os.path.exists(graphs_folder):
        os.makedirs(graphs_folder)

    # Save the graph with a unique name in the graphs folder
    filename = f'region_piechart_{region}.png'
    filepath = os.path.join(script_path,graphs_folder, filename)
    plt.savefig(filepath)

    # Optionally display the graph
    if show:
        plt.show()

    # Clear the current figure to release memory
    plt.clf()

    # Return the filepath
    print(f'{filename} is saved in {filepath}')



def countries_barchart(countries = None, show = False):
    """
    This function receives a list of countries (optional) and draws two barcharts:
    one showing the number of cases per 1 million of citizens, and the other showing
    the number of deaths per 1 million. The barcharts are saved in the ./graphs folder
    with unique names. If no countries are provided, it considers all countries in the data.
    """
    # Load data. Variables are in the following order [Country, Cases/Population, Deaths/Population, Population]
    data = cs.country_data()

    # Filter data based on the list of countries (if provided)
    if countries is not None:
        data_filtered = data[np.isin(data[:, 0], countries)]
    else:
        data_filtered = data

    # Extract columns names 
    country_names = data_filtered[:, 0]
    
    # Calculate cases and deaths per 1 million citizens
    cases_per_million = data_filtered[:, 1].astype(float) * 1_000_000
    deaths_per_million = data_filtered[:, 2].astype(float) * 1_000_000

    # Create subplots for cases per 1 million citizens and deaths per 1 million citizens
    fig, axs = plt.subplots(2, 1, figsize=(12, 12)) # 2 rows, 1 column 
    fig.subplots_adjust(hspace=0.4)

    # Bar chart for cases per 1 million citizens
    axs[0].bar(country_names, cases_per_million)
    axs[0].set_xticks(range(len(country_names))) # setting the x-axis tick locations to match the number of elements in the country_names list
    axs[0].set_xticklabels(country_names, rotation='vertical')
    axs[0].set_ylabel('Cases per 1 million')
    axs[0].set_title('COVID-19 Cases per 1 Million of Population in Countries')

    # Bar chart for deaths per 1 million citizens
    axs[1].bar(country_names, deaths_per_million)
    axs[1].set_xticks(range(len(country_names))) # # setting the x-axis tick locations to match the number of elements in the country_names list
    axs[1].set_xticklabels(country_names, rotation='vertical')
    axs[1].set_ylabel('Deaths per 1 million')
    axs[1].set_title('COVID-19 Deaths per 1 Million of Population in Countries')

    # Get the path of the script: from terminal 
    # script_path = os.path.dirname(os.path.abspath(__file__))
    
    # Get the path of the working directory
    script_path = os.getcwd()

    # Create the graphs folder if it doesn't exist
    graphs_folder = os.path.join(script_path, 'graphs')
    if not os.path.exists(graphs_folder):
        os.makedirs(graphs_folder)

    # Save the figure with subplots
    filename = 'cases_deaths_per_million.png'
    filepath = os.path.join(graphs_folder, filename)
    plt.savefig(filepath)

    # Return the filepath of the saved graph
    print(f'{filename} is saved in {filepath}')

    # Optionally display the barchart
    if show:
        plt.show()

    # Clear the current figure to release memory
    plt.clf()





def highest_mortality(k, n = 0, show = False):
    """
    This function takes two integers, n and k. It extracts the top k countries with the
    highest number of deaths per 1 million from all countries with a population size
    at least n. It then draws a bar chart for these countries.
    The argument n is optional and equals to 0 by default.
    """
    # Load data. Variables are in the following order [Country, Deaths/Population, Latitude, Longitude]
    data = cs.top_country_data(k, n)

    # Extract country names and deaths per 1 million
    country_names = data[:, 0]
    deaths_per_million = data[:, 1].astype(float) * 1_000_000

    # Create the bar chart
    plt.figure(figsize = (12, 6))
    plt.bar(country_names, deaths_per_million)
    plt.xticks(rotation = 'vertical')
    plt.ylabel('Deaths per 1 million of population')
    plt.title(f'Top {k} Countries with Highest Deaths per 1 Million of Population')
    plt.subplots_adjust(bottom=0.3) # adjusts the spacing at the bottom of the entire figure created

    # Get the path of the script: from terminal 
    # script_path = os.path.dirname(os.path.abspath(__file__))
    
    # Get the path of the working directory
    script_path = os.getcwd()

    # Create the graphs folder if it doesn't exist
    graphs_folder = os.path.join(script_path, 'graphs')
    if not os.path.exists(graphs_folder):
        os.makedirs(graphs_folder)

    # Save the plot in the graphs folder
    filename = f'top_{k}_highest_mortality_per_million.png'
    filepath = os.path.join(graphs_folder, filename)
    plt.savefig(filepath)

    # Optionally display the cases per 1 million bar chart
    if show:
        plt.show()

    # Clear the current figure to release memory
    plt.clf()

    # Return the filepaths of the saved graphs
    print(f'{filename} is saved in {filepath}')



def map(k, show = False):
    """
    This function takes an integer k as an argument and draws a map. On this map, it puts k circles
    with centers in the capital of countries with the highest number of deaths normalized by the size
    of the population. The size of the circle depends on the mortality rate.
    """
    # Load data. Variables are in the following order [Country, Deaths/Population, Latitude, Longitude]
    data = cs.top_country_data(k = k)

    # Set up the plot axes
    ax = plt.axes(projection=ccrs.PlateCarree()) #  creates a new axes and pecifies the projection of the map to be a Plate Carrée projection
    ax.stock_img()  # adds a stock image background to the map plot 

    # Iterate over all countries 
    for country in data:
        deaths_per_cap = country[1].astype(float)
        latitude = country[2].astype(float)
        longitude = country[3].astype(float)
        plt.plot(longitude, latitude, color='red', marker='o', linewidth = 0, transform=ccrs.Geodetic(),
             markersize = deaths_per_cap*500) 
        # linewidth=0 sets the linewidth of the marker outlines to zero, resulting in markers with no outlines.
        # transform=ccrs.Geodetic() specifies the coordinate transformation used for plotting the points
        
    # Set title
    plt.title(f'Top {k} Countries with Highest Mortality by COVID-19')

    # Get the path of the script: from terminal 
    # script_path = os.path.dirname(os.path.abspath(__file__))
    
    # Get the path of the working directory
    script_path = os.getcwd()

    # Create the graphs folder if it doesn't exist
    graphs_folder = os.path.join(script_path, 'graphs')
    if not os.path.exists(graphs_folder):
        os.makedirs(graphs_folder)

    # Save the plot in the graphs folder
    filename = f'top_{k}_countries_mortality_map.png'
    filepath = os.path.join(graphs_folder, filename)
    plt.savefig(filepath)

    # Optionally show the map
    if show:
        plt.show()

    # Clear the current figure to release memory
    plt.clf()

    # Return the filepaths of the saved graphs
    print(f'{filename} is saved in {filepath}')



def main():
    user_input = input("Do you want to study the coronavirus data? (Yes/No): ")
    if user_input.lower() != "yes":
        print("Thank you for using the coronavirus data tool.")
        return() # This line exits the function immediately
    
    while True: # starts an infinite loop that will keep running until a break statement is encountered
        # Ask user about the type of graph they want to plot
        graph_type = input("Which graph would you like to draw? (regions_piechart/countries_barchart/highest_mortality_barchart/highest_mortality_map): ")
        print(f"You have choosen the option: '{graph_type}'")

        # Graph 1
        if graph_type.lower() == "regions_piechart":
            region_list = cs.region_data()[:,0].tolist() # transform the whole column to list
            while True:
                region = input(f"Please choose among this list {region_list}, the region you want to study: ")
                if region in region_list:
                    break # break out of the loop and continue with the next line of code immediately following the loop
                else:
                    print("Invalid region. Please try again.")
            show = input("Do you want the graph to be shown on the screen? (Yes/No): ")
            if show.lower() == "yes":
                regions_piechart(region, show = True)
            elif show.lower() == "no":
                regions_piechart(region)
        
        # Graph 2
        elif graph_type.lower() == "countries_barchart":
            all_countries = input("Do you want the barplots of number of cases and number of deaths for ALL countries? (Yes/No): ")
            if all_countries.lower() == "no":
                countries_list = cs.read_data()[:,0].tolist()
                while True:
                    countries_input = input("Please provide the list of countries you want to plot separated by a comma without space: ")
                    countries_input = countries_input.split(',')
                    invalid_countries = []
                    for country in countries_input:
                        if country not in countries_list:
                            invalid_countries.append(country)
                    if invalid_countries:
                        print("Warning: The following countries are not in the data:", ", ".join(invalid_countries))
                    else:
                        break
                show = input("Do you want the graph to be shown on the screen? (Yes/No): ")
                if show.lower() == "yes":
                    countries_barchart(countries_input, show = True)
                else: 
                    countries_barchart(countries_input)
            elif all_countries.lower() == "yes":
                show = input("Do you want the graph to be shown on the screen? (Yes/No): ")
                if show.lower() == "yes":
                    countries_barchart(show = True)
                else: 
                    countries_barchart()

    
        # Graph 3
        elif graph_type.lower() == "highest_mortality_barchart":
            k = int(input("Please enter the number of countries: "))
            pop_threshold = input("Do you want to limit the population of the countries that you want to study? (Yes/No): ")
            if pop_threshold.lower() == "yes":
                n = int(input("Please enter the minimum size of the population: "))
                show = input("Do you want the graph to be shown on the screen? (Yes/No): ")
                if show.lower() == "yes":
                    highest_mortality(k, n, show =True)
                else: 
                    highest_mortality(k, n)
            else:
                show = input("Do you want the graph to be shown on the screen? (Yes/No): ")
                if show.lower() == "yes":
                    highest_mortality(k, show = True)
                else: 
                    highest_mortality(k)

        # Graph 4
        elif graph_type.lower() == "highest_mortality_map":
            k = int(input("Please enter the number of countries with the highest mortality that you want to be plotted on the map: "))
            show = input("Do you want the graph to be shown on the screen? (Yes/No): ")
            if show.lower() == "yes":
                map(k, True)
            else:
                map(k)
        
        else:
            print("Invalid graph type of graph. Please try again.")
        
        # Ask the user if they want to continue or quit
        user_input = input("Do you want to continue or quit? (Continue/Quit): ")
        
        if user_input.lower() == "quit":
            print("Thank you for using the coronavirus data tool! Goodbye!")
            break # breaks the first infinitive loop
    return() # This line exits the function immediately


# Call the main function when running the script
if __name__ == "__main__":
    main()


