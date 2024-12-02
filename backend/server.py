from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests

app = Flask(__name__)

# Allow your frontend's origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# New dataset URL
DATA_URL = "https://api.csvgetter.com/demo/GJIYp6QJbo1xwNR9mvLM"
data = pd.read_csv(DATA_URL)

@app.route('/multi_country_data')
def get_multi_country_data():
    visualization_type = request.args.get('type', 'co2_emissions')
    countries = ['China', 'India', 'United States']
    selected_data = data[data['country'].isin(countries)]

    result = {}
    for country in countries:
        country_data = selected_data[selected_data['country'] == country]

        if visualization_type == 'co2_emissions':
            result[country] = {
                'years': country_data['year'].tolist(),
                'values': country_data['co2'].replace({pd.NA: None, float('nan'): None}).tolist()
            }
        elif visualization_type == 'fuel_emissions':
            result[country] = {
                'years': country_data['year'].tolist(),
                'coal': country_data['coal_co2'].replace({pd.NA: None, float('nan'): None}).tolist(),
                'oil': country_data['oil_co2'].replace({pd.NA: None, float('nan'): None}).tolist(),
                'gas': country_data['gas_co2'].replace({pd.NA: None, float('nan'): None}).tolist()
            }
        elif visualization_type == 'gdp_vs_co2':
            result[country] = {
                'years': country_data['year'].tolist(),
                'gdp': country_data['gdp'].replace({pd.NA: None, float('nan'): None}).tolist(),
                'co2': country_data['co2'].replace({pd.NA: None, float('nan'): None}).tolist()
            }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
