from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Allow your frontend's origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Global datasets
DATA_URL = "https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
AIR_POLLUTION_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTxa5B5dcu0nmGheEwdrqNus2ghBe-qDz9OWUBs55pCClHTHsIfzV7QbAfId74c_J1H_l2603A6GrhZ/pub?gid=1680758461&single=true&output=csv"

# Load datasets
co2_data = pd.read_csv(DATA_URL)
air_pollution_data = pd.read_csv(AIR_POLLUTION_URL)

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
        metric = request.args.get('metric', 'deaths_per_billion')
        filter_type = request.args.get('filter', 'highest_population')

        print(f"Metric: {metric}")
        print(f"Filter Type: {filter_type}")

        air_pollution_filtered = air_pollution_data.dropna(subset=['Period', 'FactValueNumeric']).copy()


        air_pollution_filtered['Location'] = air_pollution_filtered['Location'].replace(
            {'United States of America': 'United States'}
        )


        population_data = co2_data[['country', 'year', 'population']].dropna().copy()
        population_data.rename(columns={'country': 'Location', 'year': 'Period'}, inplace=True)

        merged_df = pd.merge(
            air_pollution_filtered,
            population_data,
            on=['Location', 'Period'],
            how='inner'
        )

        print(merged_df[['FactValueNumeric', 'population']].head())


        merged_df = merged_df.dropna(subset=['FactValueNumeric', 'population'])
        merged_df = merged_df[merged_df['population'] > 0]

        if metric == 'deaths_per_billion':
            merged_df['deaths_per_billion'] = (merged_df['FactValueNumeric'] / merged_df['population']) * 1e9
        elif metric == 'deaths_per_million':
            merged_df['deaths_per_million'] = (merged_df['FactValueNumeric'] / merged_df['population']) * 1e6
        elif metric == 'total_deaths':
            merged_df['total_deaths'] = merged_df['FactValueNumeric']
        else:
            return jsonify({"error": "Invalid metric"}), 400

        print(merged_df[['FactValueNumeric', 'population', metric]].head())

        if filter_type == 'highest_population':
            sorted_data = merged_df.groupby('Location')['population'].max().sort_values(ascending=False)
        elif filter_type == 'highest_deaths':
            sorted_data = merged_df.groupby('Location')[metric].max().sort_values(ascending=False)
        elif filter_type == 'lowest_deaths':
            sorted_data = merged_df.groupby('Location')[metric].min().sort_values(ascending=True)
        else:
            return jsonify({"error": "Invalid filter option"}), 400


        print(f"Sorted Data for {filter_type}:")
        print(sorted_data.head())


        filtered_countries = sorted_data.head(3).index.tolist()
        print(f"Filtered Countries: {filtered_countries}")

        filtered_df = merged_df[merged_df['Location'].isin(filtered_countries)]

        if filtered_df.empty:
            print("No data available for the selected filter and metric.")
            return jsonify({"error": "No data available for the selected filter and metric."}), 400

     
        grouped_data = filtered_df.groupby(['Location', 'Period'])[metric].mean()

    
        print(f"Grouped Data: {grouped_data.head()}")

  
        result = grouped_data.unstack(fill_value=0).to_dict(orient='index')

        if not result:
            print("No data available for the selected filter and metric.")
            return jsonify({"error": "No data available for the selected filter and metric."}), 400

        print(result) 

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
    
@app.route('/chart_data', methods=['GET'])
def get_chart_data():
    try:
        # Step 2: Filter and preprocess air pollution data
        air_pollution = air_pollution_data[
            (air_pollution_data['Dim1'] == 'Both sexes') & 
            (air_pollution_data['Dim2'] == 'ALL CAUSES')
        ][['Location', 'Period', 'FactValueNumeric']].rename(
            columns={
                'Location': 'country',
                'Period': 'year',
                'FactValueNumeric': 'air_pollution_deaths'
            }
        )
        air_pollution['year'] = air_pollution['year'].astype(int)
        air_pollution = air_pollution.groupby(['country', 'year']).sum().reset_index()

        # Step 3: Filter emissions data
        emissions_columns = [
            'country', 'year', 'co2', 'coal_co2', 'oil_co2', 'gas_co2', 
            'cement_co2', 'methane', 'nitrous_oxide', 'total_ghg'
        ]
        emissions = co2_data[emissions_columns]

        # Merge datasets
        merged = pd.merge(air_pollution, emissions, on=['country', 'year'], how='inner')
        numeric_columns = merged.select_dtypes(include=['float64', 'int64']).columns
        merged[numeric_columns] = merged[numeric_columns].fillna(merged[numeric_columns].mean())

        # Model training
        features = ['co2', 'coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'methane', 'nitrous_oxide', 'total_ghg']
        target = 'air_pollution_deaths'
        X = merged[features]
        y = merged[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = GradientBoostingRegressor(random_state=42)
        model.fit(X_train, y_train)
        y_test_pred = model.predict(X_test)

        # Simulate 20% emission reduction
        X_test_reduced = X_test.copy()
        X_test_reduced *= 0.8
        y_reduced_pred = model.predict(X_test_reduced)

        # Prepare data for Chart.js
        actual_avg = y_test.mean()
        predicted_avg = y_test_pred.mean()
        reduced_avg = y_reduced_pred.mean()

        chart_data = {
            "labels": ["Actual Deaths", "Predicted Deaths", "Reduced Predicted Deaths"],
            "values": [actual_avg, predicted_avg, reduced_avg]
        }
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test', methods=['GET'])
def test_route():
    return "Test route works!"


if __name__ == '__main__':
    app.run(debug=True)