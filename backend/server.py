from flask import Flask, send_file, request
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/coal_consumption')
def get_image():
    country = request.args.get('country', 'China')
    url = 'https://ourworldindata.org/grapher/coal-consumption-by-country-terawatt-hours-twh.csv?v=1&csvType=full&useColumnShortNames=true'
    response = requests.get(url)
    response.raise_for_status()
    data = pd.read_csv(StringIO(response.text))
    country_data = data[data['Entity'] == country]
    plt.figure(figsize=(10, 6))
    plt.plot(country_data['Year'], country_data['coal_consumption_twh'], marker='o', linestyle='-')
    plt.title(f'Coal Consumption in {country} (TWh)')
    plt.xlabel('Year')
    plt.ylabel('Coal Consumption (TWh)')
    plt.grid(True)
    plt.savefig('coal_consumption.png')
    return send_file('coal_consumption.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)