from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import requests

app = Flask(__name__)

# Allow your frontend's origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# New dataset URL
DATA_URL = "https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
data = pd.read_csv(DATA_URL)

@app.route('/available_years')
def available_years():
    # Extract unique years from the dataset
    unique_years = data['year'].dropna().unique()
    sorted_years = sorted(unique_years)  # Sort the years for better usability

    # Convert all years to Python int type for JSON serialization
    python_years = [int(year) for year in sorted_years]

    # Convert the NumPy array directly to a list without calling tolist() again
    return jsonify(python_years)



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

@app.route('/emissions_by_year')
def emissions_by_year():
    country = request.args.get('country', 'China')
    year = int(request.args.get('year', 2020))

    # Filter data for the selected country and year
    filtered_data = data[(data['country'] == country) & (data['year'] == year)]

    if filtered_data.empty:
        return jsonify({
            "error": "No data available for the selected country and year."
        }), 404

    # Extract per capita emissions data
    emissions_per_capita = filtered_data[
        ['coal_co2_per_capita', 'flaring_co2_per_capita', 'gas_co2_per_capita', 
         'oil_co2_per_capita', 'other_co2_per_capita']
    ].fillna(0).iloc[0]

    # Return as JSON
    return jsonify({
        "country": country,
        "year": year,
        "emissions": {
            "Coal CO₂ (per capita)": emissions_per_capita['coal_co2_per_capita'],
            "Flaring CO₂ (per capita)": emissions_per_capita['flaring_co2_per_capita'],
            "Gas CO₂ (per capita)": emissions_per_capita['gas_co2_per_capita'],
            "Oil CO₂ (per capita)": emissions_per_capita['oil_co2_per_capita'],
            "Other CO₂ (per capita)": emissions_per_capita['other_co2_per_capita'],
        }
    })


@app.route('/air_pollution_data', methods=['GET'])
def get_air_pollution_data():
    try:
        # Load and process the air pollution dataset

        
        df = pd.read_csv('static/datasets/AmbientAirPollutionDeaths.csv')
        
        #Period = Year
        df['Period'] = df['Period'].astype(int)

        df = df.dropna(subset=['Period', 'FactValueNumeric']) 

        # Example processing (average PM2.5 levels by year)
        # processed_data = (df.groupby('Period')[['FactValueNumeric']].mean().to_dict())

        grouped_data = df.groupby(['Location', 'Period'])['FactValueNumeric'].mean().unstack(fill_value=0)

        data = grouped_data.to_dict(orient='index') 

        print(df[['Period', 'FactValueNumeric']].head())

        return jsonify(data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/coal_vs_air_pollution', methods=['GET'])
def get_coal_vs_air_pollution():
    try:
        # Load the air pollution dataset
        air_pollution_data = pd.read_csv('static/datasets/AmbientAirPollutionDeaths.csv')
        air_pollution_data.rename(columns={'Period': 'year', 'FactValueNumeric': 'air_pollution_deaths'}, inplace=True)

        # Filter relevant data for China
        air_pollution_data = air_pollution_data[air_pollution_data['Location'] == 'China']
        air_pollution_data = air_pollution_data[['year', 'air_pollution_deaths']]
        
        # Group and average deaths per year
        air_pollution_data = air_pollution_data.groupby('year')['air_pollution_deaths'].mean().reset_index()

        # Merge with the CO₂ emissions dataset
        china_co2_data = data[data['country'] == 'China'][['year', 'coal_co2']]
        combined_data = pd.merge(china_co2_data, air_pollution_data, on='year', how='inner')

        # Convert to JSON
        return jsonify(combined_data.to_dict(orient='list'))

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/test', methods=['GET'])
def test_route():
    return "Test route works!"

if __name__ == '__main__':
    app.run(debug=True)
