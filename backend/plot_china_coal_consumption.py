import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt

source = 'Our world in data'
# URL of the CSV file
url = 'https://ourworldindata.org/grapher/coal-consumption-by-country-terawatt-hours-twh.csv?v=1&csvType=full&useColumnShortNames=true'

# Fetch the CSV data
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Read the CSV data into a pandas DataFrame
data = pd.read_csv(StringIO(response.text))

# Filter the data for China
china_data = data[data['Entity'] == 'China']

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(china_data['Year'], china_data['coal_consumption_twh'], marker='o', linestyle='-')
plt.title('Coal Consumption in China (TWh)')
plt.xlabel('Year')
plt.ylabel('Coal Consumption (TWh)')
plt.grid(True)

# Save the plot as an image file
plt.savefig('china_coal_consumption.png')