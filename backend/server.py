from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)

# Explicitly allow your frontend's origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Your routes
DATA_URL = "https://ourworldindata.org/grapher/coal-consumption-by-country-terawatt-hours-twh.csv?v=1&csvType=full&useColumnShortNames=true"
data = pd.read_csv(DATA_URL)

@app.route('/co2_emissions')
def get_co2_emissions():
    country = request.args.get('country', 'China')  # Get the country from the request

    # Filter by the 'Entity' column instead of 'country'
    country_data = data[data['Entity'] == country]

    # If other columns like 'CO2' or 'CO2_per_capita' don't exist, adjust accordingly
    result = {
        'years': country_data['Year'].tolist(),
        'total_emissions': country_data['coal_consumption_twh'].tolist(),  # Assuming 'coal_consumption_twh' is analogous to emissions
        'per_capita_emissions': []  # Placeholder if no matching data
    }
    return jsonify(result)



@app.route('/fuel_emissions')
def get_fuel_emissions():
    country = request.args.get('country', 'China')
    # Filter by 'Entity' instead of 'country'
    country_data = data[data['Entity'] == country]

    # Update the column names based on your dataset
    result = {
        'years': country_data['Year'].tolist(),
        'coal': country_data['coal_consumption_twh'].tolist(),  # Assuming 'coal_co2' is equivalent to 'coal_consumption_twh'
        # Assuming oil and gas data are not present, provide placeholders or calculations if needed
        'oil': [],  # Placeholder if no oil data in the dataset
        'gas': []   # Placeholder if no gas data in the dataset
    }
    return jsonify(result)


@app.route('/gdp_vs_co2')
def get_gdp_vs_co2():
    country = request.args.get('country', 'China')
    # Filter by 'Entity' instead of 'country'
    country_data = data[data['Entity'] == country]

    # Placeholder data for GDP and CO₂ emissions
    result = {
        'years': country_data['Year'].tolist(),
        'gdp': [],  # Placeholder if no GDP data in the dataset
        'co2': country_data['coal_consumption_twh'].tolist()  # Assuming coal data as a proxy for CO2
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)