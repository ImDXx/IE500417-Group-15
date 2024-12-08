from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

# Allow your frontend's origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Global datasets
DATA_URL = "https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
AIR_POLLUTION_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTxa5B5dcu0nmGheEwdrqNus2ghBe-qDz9OWUBs55pCClHTHsIfzV7QbAfId74c_J1H_l2603A6GrhZ/pub?gid=1680758461&single=true&output=csv"

# Load datasets
try:
    co2_data = pd.read_csv(DATA_URL)
    air_pollution_data = pd.read_csv(AIR_POLLUTION_URL)
    air_pollution_data['Period'] = air_pollution_data['Period'].astype(int)
except Exception as e:
    raise RuntimeError(f"Error loading datasets: {e}")

@app.route('/available_years')
def available_years():
    # Extract unique years from the dataset
    unique_years = co2_data['year'].dropna().unique()
    sorted_years = sorted(unique_years)  # Sort the years for better usability

    # Convert all years to Python int type for JSON serialization
    python_years = [int(year) for year in sorted_years]

    # Convert the NumPy array directly to a list without calling tolist() again
    return jsonify(python_years)


@app.route('/multi_country_data')
def get_multi_country_data():
    visualization_type = request.args.get('type', 'co2_emissions')
    countries = ['China', 'India', 'United States']
    selected_data = co2_data[co2_data['country'].isin(countries)]

    result = {}
    for country in countries:
        country_data = selected_data[selected_data['country'] == country]
        result[country] = _get_visualization_data(country_data, visualization_type)

    return jsonify(result)


def _get_visualization_data(data, visualization_type):
    """Helper function to extract visualization data."""
    if visualization_type == 'co2_emissions':
        return {
            'years': data['year'].tolist(),
            'values': data['co2'].replace({pd.NA: None, float('nan'): None}).tolist()
        }
    elif visualization_type == 'fuel_emissions':
        return {
            'years': data['year'].tolist(),
            'coal': data['coal_co2'].replace({pd.NA: None, float('nan'): None}).tolist(),
            'oil': data['oil_co2'].replace({pd.NA: None, float('nan'): None}).tolist(),
            'gas': data['gas_co2'].replace({pd.NA: None, float('nan'): None}).tolist()
        }
    elif visualization_type == 'gdp_vs_co2':
        return {
            'years': data['year'].tolist(),
            'gdp': data['gdp'].replace({pd.NA: None, float('nan'): None}).tolist(),
            'co2': data['co2'].replace({pd.NA: None, float('nan'): None}).tolist()
        }
    return {}


@app.route('/feature_importance')
def get_feature_importance():
    china_data = co2_data[co2_data['country'] == 'China'].drop(columns=['country', 'iso_code', 'year'])
    target = 'coal_co2'
    features = china_data.drop(columns=[target]).fillna(china_data.median())
    target_data = china_data[target].fillna(china_data[target].median())

    model = RandomForestRegressor(random_state=42)
    model.fit(features, target_data)

    importance_df = pd.DataFrame({
        'Feature': features.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    return jsonify(importance_df.head(5).to_dict(orient='records'))


@app.route('/correlation_matrix')
def get_correlation_matrix():
    china_data = co2_data[co2_data['country'] == 'China'][
        ['population', 'gdp', 'co2', 'oil_co2', 'gas_co2', 'coal_co2']
    ]
    correlation_matrix = china_data.corr()['coal_co2'].sort_values(ascending=False)

    combined_results = pd.concat([correlation_matrix.head(10), correlation_matrix.tail(10)]).reset_index()
    combined_results.columns = ['Feature', 'Correlation']
    return jsonify(combined_results.to_dict(orient='records'))


@app.route('/ghg_contributors')
def get_ghg_contributors():
    china_data = co2_data[co2_data['country'] == 'China'][
        ['year', 'coal_co2', 'oil_co2', 'gas_co2', 'flaring_co2', 'other_industry_co2']
    ].fillna(0)
    return jsonify(china_data.to_dict(orient='list'))


@app.route('/emissions_by_year')
def emissions_by_year():
    country = request.args.get('country', 'China')
    year = int(request.args.get('year', 2020))

    # Filter data for the selected country and year
    filtered_data = co2_data[(co2_data['country'] == country) & (co2_data['year'] == year)]

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

        metric = request.args.get('metric','deaths_per_billion')

        # Work on a copy of the global dataset to avoid modifying the original
        air_pollution_filtered = air_pollution_data.dropna(subset=['Period', 'FactValueNumeric']).copy()

        # Replace "United States of America" with "United States"
        air_pollution_filtered['Location'] = air_pollution_filtered['Location'].replace(
            {'United States of America': 'United States'}
        )

        # Filter for the selected countries
        selected_countries = ['United States', 'India', 'China']
        air_pollution_filtered = air_pollution_filtered[air_pollution_filtered['Location'].isin(selected_countries)]

        # Prepare population data from the CO2 dataset
        population_data = co2_data[['country', 'year', 'population']].dropna().copy()
        population_data.rename(columns={'country': 'Location', 'year': 'Period'}, inplace=True)

        # Merge air pollution data with population data
        merged_df = pd.merge(
            air_pollution_filtered,
            population_data,
            on=['Location', 'Period'],
            how='inner'
        )

        # Calculate deaths per 1 billion population
        merged_df['deaths_per_billion'] = (merged_df['FactValueNumeric'] / merged_df['population']) * 1e9
        merged_df['deaths_per_million'] = (merged_df['FactValueNumeric'] / merged_df['population']) * 1e6
        merged_df['total_deaths'] = merged_df['FactValueNumeric']


        if metric not in ['total_deaths', 'deaths_per_million', 'deaths_per_billion']:
            return jsonify({"error": "Invalid metric"}), 400
        
        grouped_data = merged_df.groupby(['Location', 'Period'])[metric].mean()

        result = grouped_data.unstack(fill_value=0).to_dict(orient='index')

        return jsonify(result)

    except Exception as e:
        # Log and return error details in case of failure
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    
@app.route('/coal_vs_air_pollution', methods=['GET'])
def get_coal_vs_air_pollution():
    try:
        china_air_pollution = air_pollution_data[air_pollution_data['Location'] == 'China'][
            ['Period', 'FactValueNumeric']
        ].rename(columns={'Period': 'year', 'FactValueNumeric': 'air_pollution_deaths'}).groupby('year').mean()

        china_co2_data = co2_data[co2_data['country'] == 'China'][['year', 'coal_co2', 'co2']]
        china_co2_data['non_coal_co2'] = china_co2_data['co2'] - china_co2_data['coal_co2']

        combined_data = pd.merge(china_co2_data, china_air_pollution, on='year', how='inner')
        return jsonify(combined_data.to_dict(orient='list'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test', methods=['GET'])
def test_route():
    return "Test route works!"


if __name__ == '__main__':
    app.run(debug=True)