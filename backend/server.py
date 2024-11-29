from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/coal_consumption')
def get_coal_consumption():
    country = request.args.get('country', 'China')
    url = 'https://ourworldindata.org/grapher/coal-consumption-by-country-terawatt-hours-twh.csv?v=1&csvType=full&useColumnShortNames=true'
    response = requests.get(url)
    response.raise_for_status()
    data = pd.read_csv(StringIO(response.text))
    country_data = data[(data['Entity'] == country) & (data['Year'] >= 2000)]
    result = {
        'years': country_data['Year'].tolist(),
        'values': country_data['coal_consumption_twh'].tolist()
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)