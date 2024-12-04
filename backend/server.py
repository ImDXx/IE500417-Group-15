from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests

app = Flask(__name__)

# Allow your frontend's origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# New dataset URL
DATA_URL = "https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
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

@app.route('/feature_importance')
def get_feature_importance():
    # Load the dataset (if not already loaded)
    china_data = data[data['country'] == 'China']

    # Drop irrelevant columns
    china_data = china_data.drop(columns=['country', 'iso_code', 'year'])
    
    # Target and features
    target = 'coal_co2'
    features = china_data.drop(columns=[target])

    # Handle missing values
    features = features.fillna(features.median())
    china_data[target] = china_data[target].fillna(china_data[target].median())

    # Train RandomForest to get feature importance
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(random_state=42)
    model.fit(features, china_data[target])

    # Extract feature importance
    importances = model.feature_importances_
    importance_df = pd.DataFrame({
        'Feature': features.columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)

    # Convert to dictionary
    result = importance_df.head(5).to_dict(orient='records')  # Top 5 features

    return jsonify(result)

@app.route('/correlation_matrix')
def get_correlation_matrix():
    # Filter data for China
    china_data = data[data['country'] == 'China']

    # Specify the features to include in the correlation matrix
    selected_features = [
        'population', 'gdp', 'co2', 'oil_co2', 'gas_co2', 'coal_co2'
    ]

    # Filter the dataset to include only the selected features
    china_data = china_data[selected_features]

    # Compute correlations
    correlation_matrix = china_data.corr()

    # Filter for the target variable 'coal_co2' and sort
    coal_co2_corr = correlation_matrix['coal_co2'].sort_values(ascending=False)

    # Combine the top 10 and bottom 10 correlations
    top_10 = coal_co2_corr.head(10)  # Top 10 most positive correlations
    bottom_10 = coal_co2_corr.tail(10)  # Top 10 most negative correlations

    # Combine results
    combined_results = pd.concat([top_10, bottom_10]).reset_index()
    combined_results.columns = ['Feature', 'Correlation']

    return jsonify(combined_results.to_dict(orient='records'))

@app.route('/ghg_contributors')
def get_ghg_contributors():
    # Filter data for China
    china_data = data[data['country'] == 'China']

    # Select relevant columns
    selected_columns = ['year', 'coal_co2', 'oil_co2', 'gas_co2', 'flaring_co2', 'other_industry_co2']
    china_data = china_data[selected_columns]

    # Fill missing values with 0 for simplicity
    china_data = china_data.fillna(0)

    # Convert to JSON-friendly format
    result = china_data.to_dict(orient='list')

    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
