from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

app = Flask(__name__)

def load_data():
    try:
        # Load data with error handling
        df = pd.read_csv("travel_data.csv")
        
        # Fix headers if needed
        if "State" not in df.columns:
            df = pd.read_csv("travel_data.csv", skiprows=1)

        # Standardize column names
        df.columns = df.columns.str.strip()

        # Mapping dictionaries
        category_mapping = {
            "Mountain": 0, "Sea": 1, "Historical": 2, "Holy": 3, "Adventure": 4,
            "Cultural": 5, "Natural": 6, "Desert": 7
        }

        geo_mapping = {
            "Mountainous": 0, "Desert": 1, "Coastal": 2, "Plains": 3, "Riverine": 4,
            "Lake": 5, "Forest": 6, "Wetland": 7, "Valley": 8, "Waterfalls": 9, "Plateau": 10
        }

        # Clean and map categorical data
        df["Category"] = df["Category"].astype(str).str.strip().str.title().map(category_mapping)
        df["Geo_Type"] = df["Geo_Type"].astype(str).str.strip().str.title().map(geo_mapping)

        # Clean numerical data
        df["Climate"] = df["Climate"].astype(str).str.replace("°C", "").str.strip()
        features = ["Price", "Rating", "Popularity", "Climate"]
        df[features] = df[features].apply(pd.to_numeric, errors='coerce')
        df = df.dropna(subset=features)

        # Normalize and cluster
        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df[features])
        kmeans = KMeans(n_clusters=5, random_state=42, n_init="auto")
        df["cluster"] = kmeans.fit_predict(df_scaled)
        
        return df, category_mapping, geo_mapping
    
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None, None, None

# Initialize data
df, category_mapping, geo_mapping = load_data()

@app.route('/')
def home():
    return render_template('index2.html')
@app.route('/suggestion2')
def suggestion2():
    return render_template('Suggestion2.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if df is None:
        return render_template('results.html', message="Error: Data not loaded properly.")
    
    search_type = request.form.get('search_type')

    print(search_type)
    
    if search_type == 'state_rating':
        state_input = request.form.get('state').strip().title()
        rating_input = float(request.form.get('rating'))
        
        filtered_df = df[df["State"].str.strip().str.title() == state_input]
        filtered_df = filtered_df[filtered_df["Rating"] >= rating_input]
        
        if filtered_df.empty:
            return render_template('results.html', 
                                message=f"No matches found for state '{state_input}' with rating {rating_input} or higher.")
        
        return render_template('results.html', 
                            title=f"Recommended places in {state_input} (Rating ≥ {rating_input})",
                            results=filtered_df.to_dict('records'))
    
    elif search_type == 'category_geo':
        # Get and normalize inputs
        category_input = request.form.get('category', '').strip().title()
        geo_input = request.form.get('geo_type', '').strip().title()

        print("User inputs:", category_input, geo_input)

        # Map string inputs to numerical values
        category_num = category_mapping.get(category_input)
        geo_num = geo_mapping.get(geo_input)

        # Validate the inputs
        if category_num is None or geo_num is None:
            return render_template('results.html',
                message=f"Invalid selection. Category '{category_input}' or Geo_Type '{geo_input}' not found.")

        # Filter the dataframe
        filtered_df = df[(df["Category"] == category_num) & (df["Geo_Type"] == geo_num)]

        if filtered_df.empty:
            return render_template('results.html',
                message=f"No matches found for category '{category_input}' in {geo_input} areas.")

        return render_template('results.html',
            title=f"Recommended places ({category_input} in {geo_input} areas)",
            results=filtered_df.to_dict('records'))


    

    # # Normalize and map inputs
    # category_num = category_mapping.get(category_input.title())
    # geo_entry = geo_mapping.get(geo_input.title())
    
    # print(category_num, geo_entry)

    # # Validate inputs
    # if category_num is None or geo_entry is None:
    #     return render_template('results.html', 
    #         message=f"Invalid selection. Category '{category_input.title()}' or Geo_Type '{geo_input.title()}' not found.")

    # geo_name, geo_num = geo_entry

    # # Filter dataframe
    # filtered_df = df[(df["Category"] == category_num) & (df["Geo_Type"] == geo_num)]

    # print("filtered_df")
    # print(filtered_df)

    # if filtered_df.empty:
    #     return render_template('results.html', 
    #         message=f"No matches found for category '{category_input.title()}' in {geo_name} areas.")

    # return render_template('results.html', 
    #     title=f"Recommended places ({category_input.title()} in {geo_name} areas)",
    #     results=filtered_df.to_dict('records'))

    
    # return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)